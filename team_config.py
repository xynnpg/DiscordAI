# Team configuration
# Add your team member usernames here (Discord usernames, not display names)
TEAM_MEMBERS = [
    "xynnpg",  # Your username
    # Add more team members here as needed
    # "username2",
    # "username3",
]

def is_team_member(username):
    """Check if a username is a team member"""
    return username.lower() in [member.lower() for member in TEAM_MEMBERS]

def get_team_members():
    """Get list of team members"""
    return TEAM_MEMBERS 