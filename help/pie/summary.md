*__PIE — Programmable Image Edit__*

Python-based English and Russian programming language designed to help edit images in telegram.

Images may be resized to fit 2560 px square to meet telegram restrictions.

PIE program is a text argument to `.pie` command (the prefix is necessary). AlterPy can execute PIE code from attached reply if no text is given in main message.

Pie command handler requires image to be attached in the message or in the reply. Albums can't be processed.

PIE can see only two pictures from messages — the message one, `msg`, and the reply one, `rep`. If there is no picture attached to message, then `msg` is set equal to `rep`. If there is no reply or there is no image in it, then `rep` will be set to `None` and any commands using it will fail.

Pie commands can be written in both English and Russian. This help covers English commands.

Every command is written on its own line, empty lines are ignored. If at least one command can't be parsed, the code won't be executed and the error will be shown.

You can find help pages for commands using `no lmao working in progress` command.

Pie commands are case-insensitive, for example, `send`, `SEND` and `sEnD` are the same command.

Variable names can use digits, English and Russian letters. Variable name can't start with a digit.

If an error occurs at run time you will receive a message with exception details and your code translated to Python to debug the error.

Example pie program: Send diminished image and grey image as file

```
.pie
decrease msg 2 fold to first
gray msg to second
send first
file second
```

For this program to work an image should be provided, either attached to message or to a reply.

PIE is unable to determine which pictures are the result ones — sending the result is a writer's concern, and not AlterPy's one.

Detailed help on commands is coming soon...
