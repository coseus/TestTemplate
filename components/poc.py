# components/poc.py
import streamlit as st
import base64

def render():
    st.subheader("Proof of Concept (Manual)")

    # === ADD NEW POC ===
    with st.expander("Add New PoC", expanded=False):
        title = st.text_input("PoC Title", placeholder="PoC-001", key="poc_add_title")
        desc = st.text_area("Description", height=100, key="poc_add_desc")
        code = st.text_area("Code / Exploit", height=150, key="poc_add_code")
        uploaded_images = st.file_uploader("Screenshots", accept_multiple_files=True, type=["png", "jpg", "jpeg"], key="poc_add_images")

        if st.button("Add PoC", key="poc_add_btn"):
            if not title.strip():
                st.error("Title required!")
            else:
                images_b64 = []
                for img in uploaded_images:
                    try:
                        img_bytes = img.read()
                        img_type = img.type
                        ext = img_type.split("/")[-1].split(";")[0]
                        b64_str = f"data:image/{ext};base64,{base64.b64encode(img_bytes).decode()}"
                        images_b64.append(b64_str)
                    except Exception as e:
                        st.error(f"Invalid image {img.name}: {e}")

                new_poc = {
                    "title": title,
                    "description": desc,
                    "code": code,
                    "images": images_b64
                }
                st.session_state.poc_list.append(new_poc)
                st.success("PoC added!")
                st.rerun()

    # === LISTĂ POC ===
    for idx, poc in enumerate(st.session_state.poc_list):
        with st.expander(f"{poc['title']} (ID: {idx})", expanded=False):
            st.write(poc.get("description", ""))
            if poc.get("code"):
                st.code(poc["code"], language=None)

            # === IMAGINI ===
            if poc.get("images"):
                cols = st.columns(3)
                for img_idx, img_b64 in enumerate(poc["images"]):
                    with cols[img_idx % 3]:
                        if img_b64.startswith("data:image"):
                            try:
                                _, b64_data = img_b64.split(",", 1)
                                img_bytes = base64.b64decode(b64_data)
                                st.image(img_bytes, use_column_width=True)
                            except:
                                st.write("[Corrupted image]")

            if st.button("Delete", key=f"del_poc_{idx}"):
                st.session_state.poc_list.pop(idx)
                st.rerun()
