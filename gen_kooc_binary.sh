#!/bin/bash

function check_folder
{
	if [[ -f kooc.py ]]; then
		return
	fi
	echo "You must run this script in kooc project source, exiting.."
	exit 42
}

function generate_kooc
{
	echo -e "#!/bin/sh\n$PWD/kooc.py" '$*' > "$KOOC_NAME"
	chmod +x "$KOOC_NAME"
}

KOOC_NAME=kooc

check_folder
generate_kooc

echo "Standalone '$KOOC_NAME' binary generated"
echo "You can now move it where you want and execute it:"
echo "   $ cp $KOOC_NAME ~/.bin"
echo "   $ $KOOC_NAME some.kh files.kc      # Assuming ~/.bin is in your PATH"

