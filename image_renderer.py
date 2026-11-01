import base64
import io
import streamlit as st


def render_matplotlib_base64(fig, width="100%", dpi=150):
    """
    Render a Matplotlib figure as an embedded Base64 PNG.
    This avoids Streamlit's /media/ image endpoint.
    """
    buffer = io.BytesIO()

    fig.savefig(
        buffer,
        format="png",
        bbox_inches="tight",
        dpi=dpi
    )

    encoded = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    buffer.close()

    st.markdown(
        f"""
        <div style="width:100%; overflow:hidden;">
            <img
                src="data:image/png;base64,{encoded}"
                style="
                    display:block;
                    width:{width};
                    max-width:100%;
                    height:auto;
                    border-radius:8px;
                "
            />
        </div>
        """,
        unsafe_allow_html=True
    )
