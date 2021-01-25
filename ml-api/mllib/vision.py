try:
    import sys
    import os

    sys.path.append("/mnt/efs/lib")  # nopep8 # noqa
except ImportError:
    pass

try:
    import unzip_requirements
except ImportError:
    pass

import json
import io
import base64
import torch
from PIL import Image
from torchvision import transforms
from requests_toolbelt.multipart import decoder

print(f"Pytorch version - {torch.__version__}")

torch.hub.set_dir("/mnt/efs/.cache")
model = torch.hub.load("pytorch/vision:v0.6.0", "deeplabv3_resnet101", pretrained=True)
model.eval()

print("Model is loaded successfully.")

IMG_SIZE = 512


def base64_encode_img(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)
    img_byte = buffered.getvalue()
    # encoded_img_str = "data:image/png;base64," + base64.b64encode(img_byte).decode()
    encoded_img_str = base64.b64encode(img_byte).decode()
    return encoded_img_str


def get_segments(input_image):
    width, height = input_image.size
    resize_factor = min(IMG_SIZE / width, IMG_SIZE / height)
    input_image = input_image.resize(
        (
            int(input_image.width * resize_factor),
            int(input_image.height * resize_factor),
        )
    )
    preprocess = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    input_tensor = preprocess(input_image)

    # create a mini-batch as expected by the model
    input_batch = input_tensor.unsqueeze(0)

    # move the input and model to GPU for speed if available
    if torch.cuda.is_available():
        input_batch = input_batch.to("cuda")
        model.to("cuda")

    with torch.no_grad():
        output = model(input_batch)["out"][0]
    output_predictions = output.argmax(0)

    # create a color pallette, selecting a color for each class
    palette = torch.tensor([2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1])
    colors = torch.as_tensor([i for i in range(21)])[:, None] * palette
    colors = (colors % 255).numpy().astype("uint8")

    # plot the semantic segmentation predictions of 21 classes in each color
    segments = Image.fromarray(output_predictions.byte().cpu().numpy()).resize(
        input_image.size
    )
    segments.putpalette(colors)
    return segments


def predict(event, context):
    input_image = None
    content_type_header = event["headers"]["content-type"]
    body = event["body"].encode()

    for part in decoder.MultipartDecoder(body, content_type_header).parts:
        content_type_part = part.headers[b"content-type"]
        if (
            b"image/png" in content_type_part
            or b"image/jpg" in content_type_part
            or b"image/jpeg" in content_type_part
        ):
            input_image = Image.open(io.BytesIO(part.content)).convert("RGB")

    if input_image is None:
        raise RuntimeError("No image provided")

    return get_segments(input_image)


def main(event, context):

    # warm up
    if event and event.get("source") in ["aws.events", "serverless-plugin-warmup"]:
        print("Lambda container is up and running")
        return {}

    try:
        output_image = predict(event, context)
        response = {
            "statusCode": 200,
            # "body": json.dumps({"image": base64_encode_img(output_image)}),
            "body": base64_encode_img(output_image),
            "isBase64Encoded": True,
            "headers": {
                "Content-Type": "application/png",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
        }
        # print(response)
        return response
    except RuntimeError as e:
        response = {
            "statusCode": 500,
            "body": json.dumps({"error": e}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
        }
        return response
