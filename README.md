# groupme-slack
In 2019 I was President of a club that used GroupMe as our main communication platform. We ran into an issue where most users would mute the GroupMe to avoid notification spam, and therefore were not notified of more important communications. I decided to migrate the club to Slack so that users could mute individual channels while leaving the announcements channel unmuted. Because most users had GroupMe muted however, it wasn't feasible to have everyone switch apps all at once.

To facilitate a gradual migration, I wrote this tool. It's a simple bot that copies messages from Slack to GroupMe and vice versa. I ended up running this tool for ~a month and a half, which cost me ~$7 on an AWS t2 micro. Way cheaper than sameroom.io

There's a few bugs with it, and I wouldn't use it outside a club environment. If I find myself needing a tool like this again in the future I'll probably re-write. One thing I'd like to get away from is having to register so many [GroupMe](https://dev.groupme.com/tutorials/bots) and [Slack](https://api.slack.com/start) bots/plugins.
