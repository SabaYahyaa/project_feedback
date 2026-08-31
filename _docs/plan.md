MVP scope
1. Users and roles

Admin/Manager

Creates a project.
Adds/removes team members.
Sets the retrospective time.
Can view the project feedback.

Team member

Submits weekly feedback.
Can edit it until Friday 10:00.
Can choose anonymous or attributed.

Why: This keeps permissions simple and avoids building a complicated role system.

2. Weekly cycle

Monday → Friday 10:00

Feedback can be submitted or edited anytime.

Friday 10:00

Feedback automatically closes.
No more editing/submission.

Friday 11:30

Team retrospective.

Why: The system has a very clear lifecycle, which makes both the user experience and implementation much easier.

3. Feedback form

Each submission contains:

Weekly update

What I worked on
Progress

Reflection

What worked well?
What didn't work / blockers?
What could be improved?
Suggestions
Other feedback

And:

☐ Submit anonymously

Why: This gives enough structure to make feedback useful while still allowing people to speak honestly.

4. Retrospective

The retrospective has two views:

Feedback Board

What worked
What didn't
Improvements
Suggestions
Other

Meeting View

Discuss feedback
Record decisions
Record action items
Description
Owner
Deadline

Why: The board is for understanding the feedback; the meeting view is for turning discussion into concrete outcomes.

5. History

Keep only the current weekly cycle.

After the retrospective, that week's information is discarded.

Why: You explicitly want this for the MVP, and it dramatically reduces storage, privacy, and historical-data complexity.

6. Missing feedback

I would choose C: reminders + optional submission.

For example:

Wednesday: reminder
Thursday: reminder
Friday 09:00: final reminder

People are never forced to submit.

Why: The tool should encourage participation, not become another mandatory administrative task.

7. Important MVP principle

I would not add AI yet.

No automatic summaries, sentiment analysis, recommendations, trend detection, Slack/Teams integration, dashboards, etc.

Why: The core question for version 1 is:

Can a team use this tool every week to collect honest feedback and have a useful retrospective?

We should prove that workflow first. AI can become a V2 feature once we know what information teams actually need.

The MVP in one sentence

A project-based weekly feedback tool where team members submit structured attributed or anonymous feedback during the week, the system closes submissions every Friday at 10:00, and the team uses the collected feedback in an 11:30 retrospective to record decisions and action items.