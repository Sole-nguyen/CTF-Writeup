# caas_jupyter_tools.py (shim fallback)
# Cung cấp một hàm display_dataframe_to_user đơn giản để thay thế
def display_dataframe_to_user(name, dataframe):
    """
    Simple fallback: print a header and then attempt to pretty-print a pandas DataFrame,
    otherwise print repr() of the object.
    """
    try:
        print("=" * 60)
        print("DISPLAY:", name)
        print("-" * 60)
        # if it's pandas DataFrame, to_string prints nicely
        print(dataframe.to_string())
        print("=" * 60)
    except Exception:
        # fallback generic
        try:
            # if object supports iterrows (pandas), try to show first rows
            rows = list(dataframe)[:10]
            print(repr(rows))
        except Exception:
            print(repr(dataframe))
