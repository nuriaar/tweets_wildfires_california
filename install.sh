echo -e "Installing the virtual environment..."
python3 -m venv virtual_larry
source virtual_larry/bin/activate
pip3 install -r requirements.txt
deactivate
echo -e "Virtual environment is ready!"
