# components/scope.py
import streamlit as st

def render():
    st.subheader("Scope of Testing")

    # === IN-SCOPE ===
    scope_in = st.text_area(
        "In-Scope",
        value=st.session_state.get("scope_in", ""),
        height=100,
        key=None  # ← ELIMINAT key!
    )

    # === OUT-OF-SCOPE ===
    scope_out = st.text_area(
        "Out-of-Scope",
        value=st.session_state.get("scope_out", ""),
        height=100,
        key=None  # ← ELIMINAT key!
    )

    # === CLIENT ALLOWANCES ===
    allowances = st.text_area(
        "Client Allowances",
        value=st.session_state.get("allowances", ""),
        height=100,
        key=None  # ← ELIMINAT key!
    )

    # === SAVE BUTTON ===
    if st.button("Save Scope", type="primary"):
        # Salvează în session_state
        st.session_state.scope_in = scope_in
        st.session_state.scope_out = scope_out
        st.session_state.allowances = allowances

        # Creează un singur string pentru PDF
        full_scope = f"""
**In-Scope:**  
{scope_in or "N/A"}

**Out-of-Scope:**  
{scope_out or "N/A"}

**Client Allowances:**  
{allowances or "N/A"}
        """.strip()
        st.session_state.scope = full_scope

        st.success("Scope saved!")
        st.rerun()
