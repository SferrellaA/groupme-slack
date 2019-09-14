# groupme-slack
I wrote this tool for a club I was a member of. We used to use groupme for club communications, but ran into a problem where we had so many members that most of them muted the groupme to avoid the flood of notifications. Because everyone had the groupme muted, they didn't get the actual announcements we had. In effect, we had no communication method that could reliably be used to reach our members.

I decided we'd move to Slack, as users could then mute individual channels while leaving an #announcements channel alone. I figured that because we had so many muted members though, that they wouldn't get the memo about the move. Awk.

So I wrote this. It's just a simple bot that copies messages from Slack and GroupMe and copies them into the other. It's a little buggy, breaking when users edit messages for example, but it was useful for our needs at the time. A month and a half into the transition, we had nearly all of our members in Slack, so we shut the thing down and now I don't care about it.

I ran our instance of the bot on AWS. It cost me under $3/mo, so that was nice. I did have to register a Slack plugin (a private one), as well as create a groupme bot for each channel that was being synced. Not super convenient to set up, but still a lot cheaper than soemthing like sameroom.io
