#deletes all .ipynb_checkpoints so they are not uploaded to GCP storage
rm -rf `find -type d -name .ipynb_checkpoints`
