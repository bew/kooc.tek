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
	echo -e "#!/bin/sh\n$PWD/kooc.py" '$*' > koocexe
	chmod +x koocexe
}

check_folder
generate_kooc

echo "Standalone 'kooc' binary generated"
echo "You can now move it where you want and execute it:"
echo "   $ cp kooc ~/.bin"
echo "   $ kooc some.kh files.kc      # Assuming ~/.bin is in your PATH"
