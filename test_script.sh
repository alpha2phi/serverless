curl -X POST -H "Content-Type: multipart/form-data" \
    -F "image=@test_images/deeplab1.png" \
  https://5juixetc81.execute-api.ap-southeast-1.amazonaws.com/vision -o output.png


  # http://localhost:3000/dev/vision -o output.png
