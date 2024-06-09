# Quibble
Discord weather and game bot. Invite_link : https://discord.com/oauth2/authorize?client_id=1247624200655601686&amp;permissions=843961281600&amp;scope=bot

;{command} :: private messaging
\n
\>{command} :: channel messaging

\>weather {location} :: get the weather at your favorite place.
      fetches weather conditions of the specified place using weather api in a json format, which is then unwrapped into python object and send as an embedded message to the channel from which request was send

\>ttt {user_id} :: challenge a friend in the channel for a Tic Tac Toe match.
      Python creates a game object containing current user, opponent and ttt layout, which is added to a hashtable mapping message id and game object. On giving reaction mentioned by the bot, the corresponding square is updated via array updation which is joined to form the display string(ttt grid) in the channel. Using a hashtable avoids multiple users accessing the same instance of the game. 
