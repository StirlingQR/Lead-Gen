streamlit.runtime.media_file_storage.MediaFileStorageError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/lead-gen/app.py", line 84, in <module>
    display_logo()
File "/mount/src/lead-gen/app.py", line 36, in display_logo
    st.image(str(LOGO_PATH), use_container_width=True)
File "/home/adminuser/venv/lib/python3.12/site-packages/streamlit/runtime/metrics_util.py", line 410, in wrapped_func
    result = non_optional_func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/streamlit/elements/image.py", line 181, in image
    marshall_images(
File "/home/adminuser/venv/lib/python3.12/site-packages/streamlit/elements/lib/image_utils.py", line 439, in marshall_images
    proto_img.url = image_to_url(
                    ^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/streamlit/elements/lib/image_utils.py", line 298, in image_to_url
    url = runtime.get_instance().media_file_mgr.add(image, mimetype, image_id)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/streamlit/runtime/media_file_manager.py", line 226, in add
    file_id = self._storage.load_and_get_id(
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/streamlit/runtime/memory_media_file_storage.py", line 115, in load_and_get_id
    file_data = self._read_file(path_or_data)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.12/site-packages/streamlit/runtime/memory_media_file_storage.py", line 167, in _read_file
    raise MediaFileStorageError(f"Error opening '{filename}'") from ex
