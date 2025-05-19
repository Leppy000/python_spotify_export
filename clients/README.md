# How to authenticate
I'm currently using the `ngrok` to get authentication secret from Spotify because, otherwise, it would impossible to add a non-secure callback on the `http` protocol.

## How to install `ngrok`
In you local bash script launch the following command:
```bash
curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
  && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list \
  && sudo apt update \
  && sudo apt install ngrok
```

## How to configure and launch `ngrok`
Get your custom token from your `ngrok` dashboard (https://dashboard.ngrok.com/get-started/your-authtoken)
```
export NGROK_TOKEN=<YOUR-NGROK-TOKEN>
ngrok config add-authtoken $NGROK_TOKEN
```
**_NOTE:_** if everything goes fine, you should see the token saved under:
`/home/<your-dir>/.config/ngrok/ngrok.yml`

Now you can start `ngrok` so that it listens to the 8888 port and can intercept for you the spotify auth-token
```
ngrok http 8888
```
This should start the `ngrok` console

## Local deployment
For local deployment is not a real issue, the reason is simple: it's a local script and if an hacker would want take the token he should do it within my network :)