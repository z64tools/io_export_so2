

release:
	rm -f io_export_so2.zip
	cp __init__.py io_export_so2/__init__.py
	cp export.py io_export_so2/export.py
	cp interface.py io_export_so2/interface.py
	cp node_setup.py io_export_so2/node_setup.py
	cp properties.py io_export_so2/properties.py
	zip -r io_export_so2.zip io_export_so2