echo "Linting..."

if flake8; then
  echo -e "\e[92m===== flake8 ok\e[39m"
else
  echo -e "\e[91m===== flake8 failed\e[39m"
  exit
fi

detox
sleep 1
