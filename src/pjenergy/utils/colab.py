
def is_in_colab() -> bool:

    try:
        import google.colab # type: ignore
        IN_COLAB = True
    except:
        IN_COLAB = False

    return IN_COLAB
