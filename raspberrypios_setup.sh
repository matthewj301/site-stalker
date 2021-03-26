curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Assuming the 'pi' user is being used
sudo usermod -aG docker pi

sudo apt install git

git clone https://github.com/matthewj301/site-stalker.git

cd site-stalker

docker build -t sitestalker-prod . && docker run --name sitestalker --rm --net=host sitestalker-prod:latest
