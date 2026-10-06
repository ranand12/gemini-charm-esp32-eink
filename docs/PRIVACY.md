# Export and privacy

Included: latest saved v3.2 application source, required drivers/vendor source and licenses, public CA certificates, build/settings examples, setup helper and documentation.

Excluded: compiled firmware and full-flash images, NVS/device snapshots, logs and transcripts, old source backups, personal paths/board identity, real credentials and API keys. Original private service URL replaced with a local configurable endpoint. Original files remain untouched. Repository starts with fresh Git history.

The only configuration example is a placeholder endpoint. Credentials are provided at runtime over USB serial; they are stored on the board, not in this repository. Public CA certificates are trust anchors, not private keys. Upstream copyright attribution is retained.

Keep `local_config.h`, build output, serial logs and device backups private and outside version control. NVS is not encrypted by this application. Anyone with physical access to a board/flash backup may be able to recover credentials. Serial output can contain Wi-Fi names, task IDs and response text.
