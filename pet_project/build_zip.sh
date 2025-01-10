rm lambda_function.zip


rm -r deps
# Step 1: Install dependencies into the "deps" folder
pip3 install -r requirements.txt -t deps/

# Step 2: Create a temporary folder to prepare files for the zip archive
mkdir -p build

# Step 3: Copy all files from "deps" into the build folder
cp -r deps/* build/

# Step 4: Copy all files from the current directory (excluding folders) into the build folder
cp * build/

# Step 5: Create the zip archive from the build folder's content
cd build
zip -r ../lambda_function.zip .

# Step 6: Clean up the temporary build folder
cd ..
rm -rf build
