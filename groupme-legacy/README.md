#groupme-legacy

So when we finished the migration of our club members from GroupMe to Slack, there were still a handful of members that hadn't migrated. I wasn't sure if they were old members that had moved, if they somehow hadn't heard about the move, or if they were just being stubborn. I decided to make something that would address all of these thigns.

I essentially just stripped out the Slack components of groupme-slack, and made it so that a groupme message was sent whenever a groupme message was received. My club has it sending a reminder that we've migrated to Slack whenever someone posts to the groupme, including an invite link for it. 

Do note though, that a groupme "message" includes the message generated when a member leaves the group. If someone leaves because they can't take the spam of automatic messages, they might very well cause another to leave. By my math, the old groupme will be cleaned out within a month. 
