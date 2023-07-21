## Creating ngrok tunnel

1. Create ngrok account and create free endpoint at https://dashboard.ngrok.com/cloud-edge/endpoints
2. Define a route for `/interaction`, copy the edge label from the newly created route
3. Copy `ngrok.yml.example` in `./local` to `ngrok.yml`
4. substitute `NGROK_TUNNEL_LABEL` for the route label from 2, also substitute `NGROK_AUTH_TOKEN` for your auth token

## Registering discord application

1. Create a new discord application
2. Define `DISCORD_CLIENT_ID`, `DISCORD_CLIENT_SECRET`, `DISCORD_PUBLIC_KEY` based on the variables provided by discord (put in .env prefixed by FLASK_)
3. Run `python app.py`
4. Start ngrok tunnel
5. Enter `{ngrok_endpoint_url}/interaction/` as the "interactions endpoint url"
6. Save changes, if it succeeds you've succesfully registered the endpoint.


See https://flask-discord-interactions.readthedocs.io/en/latest/botsetup.html for a more thorough guide