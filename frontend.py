import streamlit as st
import os
import subprocess
import glob
from PIL import Image
import time

# Set page configuration
st.set_page_config(
    page_title="Graph-6G-Network",
    page_icon="📊",
    layout="wide"
)

# App title
st.title("📊 Knowledge Graph based End to End 6G Design process")
st.markdown("---")

# Create columns for better layout
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📁 File Selection")
    
    # File uploader - allows multiple files
    uploaded_files = st.file_uploader(
        "Choose files to process",
        accept_multiple_files=True,
        type=['csv', 'txt', 'json', 'xlsx', 'png', 'jpg', 'jpeg']
    )
    
    # Display selected files
    if uploaded_files:
        st.success(f"Selected {len(uploaded_files)} file(s):")
        for file in uploaded_files:
            st.write(f"• {file.name} ({file.size} bytes)")
    
    st.markdown("---")
    
    # Configuration options
    st.header("⚙️ Processing Options")
    
    # Python script selection
    python_script = st.selectbox(
        "Select Python script to run:",
        ["kgmethod_updated.py"],
        help="Choose the Python script that will process your files"
    )
    
    # Fixed output folder (same as frontend code location)
    output_folder = "."
    
    st.markdown("---")
    
    # Process button
    process_button = st.button(
        "🚀 Run Processing",
        type="primary",
        use_container_width=True,
        disabled=not uploaded_files
    )

with col2:
    st.header("📊 Results Visualization")
    
    if process_button and uploaded_files:
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Save uploaded files to temporary directory
            status_text.text("Saving uploaded files...")
            progress_bar.progress(20)
            
            temp_dir = "./temp_input"
            os.makedirs(temp_dir, exist_ok=True)
            
            saved_files = []
            for uploaded_file in uploaded_files:
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                saved_files.append(file_path)
            
            # Step 2: Create output directory
            status_text.text("Creating output directory...")
            progress_bar.progress(40)
            os.makedirs(output_folder, exist_ok=True)
            
            # Step 3: Run the Python script
            status_text.text(f"Running {python_script}...")
            progress_bar.progress(60)
            
            # Run the Python script without any command line parameters
            cmd = ["python", python_script]
            
            # Execute the actual Python script
            subprocess.run(cmd, check=True)
            
            # Step 4: Processing complete
            status_text.text("Processing complete!")
            progress_bar.progress(100)
            
            st.success("✅ Processing completed successfully!")
            
            # Step 5: Display generated images
            st.subheader("Generated Images:")
            
            # Get all image files from output folder
            image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']
            image_files = []
            for ext in image_extensions:
                image_files.extend(glob.glob(os.path.join(output_folder, ext)))
            
            if image_files:
                # Sort files by creation time (newest first)
                image_files.sort(key=os.path.getctime, reverse=True)
                
                # Display images in a grid
                cols = st.columns(2)
                for idx, img_path in enumerate(image_files):
                    try:
                        img = Image.open(img_path)
                        col_idx = idx % 2
                        
                        with cols[col_idx]:
                            st.image(
                                img, 
                                caption=os.path.basename(img_path),
                                use_container_width=True
                            )
                            
                            # Add download button for each image
                            with open(img_path, "rb") as file:
                                st.download_button(
                                    label=f"Download {os.path.basename(img_path)}",
                                    data=file.read(),
                                    file_name=os.path.basename(img_path),
                                    mime="image/png",
                                    key=f"download_{idx}"
                                )
                    except Exception as e:
                        st.error(f"Error loading image {img_path}: {str(e)}")
                
                # Summary statistics
                st.subheader("📈 Processing Summary")
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("Files Processed", len(uploaded_files))
                
                with col_b:
                    st.metric("Images Generated", len(image_files))
                
                with col_c:
                    total_size = sum(os.path.getsize(f) for f in image_files)
                    st.metric("Total Output Size", f"{total_size/1024:.1f} KB")
                
            else:
                st.warning("No images found in the output folder.")
                st.info(f"Looking for images in: {output_folder}")
        
        except subprocess.CalledProcessError as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"Error running Python script: {e}")
            st.code(f"Command that failed: {' '.join(cmd)}")
        
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"An error occurred: {str(e)}")
    
    elif not uploaded_files:
        st.info("👆 Please select files to process")
        
        # Only show existing images when no files are uploaded
        if os.path.exists(output_folder):
            image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp']
            existing_images = []
            for ext in image_extensions:
                existing_images.extend(glob.glob(os.path.join(output_folder, ext)))
            
            if existing_images:
                st.subheader("Previously Generated Images:")
                existing_images.sort(key=os.path.getctime, reverse=True)
                
                cols = st.columns(2)
                for idx, img_path in enumerate(existing_images[:4]):  # Show max 4 previous images
                    try:
                        img = Image.open(img_path)
                        col_idx = idx % 2
                        
                        with cols[col_idx]:
                            st.image(
                                img, 
                                caption=f"Previous: {os.path.basename(img_path)}",
                                use_container_width=True
                            )
                    except Exception as e:
                        pass

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "File Processing & Visualization App | Built with Streamlit"
    "</div>", 
    unsafe_allow_html=True
)