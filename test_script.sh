curl -X POST -H "Content-Type: multipart/form-data" \
    -F "image=@test_images/deeplab1.png" http://localhost:3000/dev/vision -o output.png
