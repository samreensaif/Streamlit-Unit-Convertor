def enqueue(self, msg: ForwardMsg) -> None:
    """Enqueue a ForwardMsg for this context's session."""
    if msg.HasField("page_config_changed") and not self._set_page_config_allowed:
        raise StreamlitSetPageConfigMustBeFirstCommandError()

    # We want to disallow set_page config if one of the following occurs:
    # - set_page_config was called on this message
    # - The script has already started and a different st call occurs (a delta)
    if msg.HasField("page_config_changed") or (
        msg.HasField("delta") and self._has_script_started
    ):
        self._set_page_config_allowed = False 