"""
Sample names pool for generating random attendees.
"""

# Pool of random, creative names for sample data
SAMPLE_NAMES = [
    "Alex Carter", "Morgan Blake", "Taylor Reed", "Casey Stone",
    "Jordan Hayes", "Jamie Brooks", "Avery Lane",
    "Cameron Wells", "Drew Parker", "Skyler James", "Reese Morgan",
    "Quinn Taylor", "Logan Blair", "Rowan Ellis", "Emerson Gray",
    "Finley Hart", "Harper Knox", "Sage Monroe", "Dakota Flynn",
    "Peyton Rivers", "Charlie West", "Jules Bennett", "Micah Ford",
    "Tatum Kelly", "Elliot Marsh", "Blair Ramsey", "Shiloh Dean",
    "Lennon Burke", "Remy Chandler", "Kendall Frost", "Phoenix Tate",
    "Sawyer Bell", "River Sloan", "Frankie Lowell", "Marley Vaughn",
    "Noel Jennings", "Justice Hale", "Oakley Pierce", "Rowan Tate",
    "Ellis Jordan", "Spencer Cole", "Quincy Drew", "Aubrey Shaw",
    "Devon Miles", "Rory Bennett", "Shay Douglas", "Toby Grant",
    "Jesse Lane", "Cory Mason", "Emery Scott", "Blake Avery",
    "Casey Monroe", "Taylor Quinn", "Jamie Ellis", "Morgan Reese",
    "Alex Jordan", "Riley Blair", "Skyler Hayes", "Avery Brooks",
    "Cameron Lane", "Drew Wells", "Reese Parker", "Quinn James",
    "Logan Morgan", "Rowan Taylor", "Emerson Blair", "Finley Ellis",
    "Harper Gray", "Sage Hart", "Dakota Knox", "Peyton Monroe",
    "Charlie Flynn", "Jules Rivers", "Micah West", "Tatum Bennett",
    "Elliot Ford", "Blair Kelly", "Shiloh Marsh", "Lennon Ramsey",
    "Remy Dean", "Kendall Burke", "Phoenix Chandler", "Sawyer Frost",
    "River Tate", "Frankie Bell", "Marley Sloan", "Noel Lowell",
    "Justice Vaughn", "Oakley Jennings", "Rowan Hale", "Ellis Pierce",
    "Spencer Tate", "Quincy Jordan", "Aubrey Cole", "Devon Drew",
    "Rory Shaw", "Shay Miles", "Toby Bennett", "Jesse Douglas",
    "Cory Grant", "Emery Lane", "Blake Mason", "Casey Scott",
    "Taylor Avery", "Jamie Monroe", "Morgan Quinn", "Alex Ellis",
    "Riley Reese", "Skyler Jordan", "Avery Blair", "Cameron Hayes",
    "Drew Brooks", "Reese Lane", "Quinn Wells", "Logan Parker",
    "Rowan James", "Emerson Morgan", "Finley Taylor", "Harper Blair",
    "Sage Ellis", "Dakota Gray", "Peyton Hart", "Charlie Knox",
    "Jules Monroe", "Micah Flynn", "Tatum Rivers", "Elliot West",
    "Blair Bennett", "Shiloh Ford", "Lennon Kelly", "Remy Marsh",
    "Kendall Ramsey", "Phoenix Dean", "Sawyer Burke", "River Chandler",
    "Frankie Frost", "Marley Tate", "Noel Bell", "Justice Sloan",
    "Oakley Lowell", "Rowan Vaughn", "Ellis Jennings", "Spencer Hale",
    "Quincy Pierce", "Aubrey Tate", "Devon Jordan", "Rory Cole",
    "Shay Drew", "Toby Shaw", "Jesse Miles", "Cory Bennett",
    "Emery Douglas", "Blake Grant", "Casey Lane", "Taylor Mason",
    "Jamie Scott", "Morgan Avery", "Alex Monroe", "Riley Quinn",
    "Skyler Ellis", "Avery Reese", "Cameron Jordan", "Drew Blair",
    "Reese Hayes", "Quinn Brooks", "Logan Lane", "Rowan Wells",
    "Emerson Parker", "Finley James", "Harper Morgan", "Sage Taylor",
    "Dakota Blair", "Peyton Ellis", "Charlie Gray", "Jules Hart",
    "Micah Knox", "Tatum Monroe", "Elliot Flynn", "Blair Rivers",
    "Shiloh West", "Lennon Bennett", "Remy Ford", "Kendall Kelly",
    "Phoenix Marsh", "Sawyer Ramsey", "River Dean", "Frankie Burke",
    "Marley Chandler", "Noel Frost", "Justice Tate", "Oakley Bell",
    "Rowan Sloan", "Ellis Lowell", "Spencer Vaughn", "Quincy Jennings",
    "Aubrey Hale", "Devon Pierce", "Rory Tate", "Shay Jordan",
    "Toby Cole", "Jesse Drew", "Cory Shaw", "Emery Miles",
    "Blake Bennett", "Casey Douglas", "Taylor Grant", "Jamie Lane",
    "Morgan Mason", "Alex Scott", "Riley Avery", "Skyler Monroe",
    "Avery Quinn", "Cameron Ellis", "Drew Reese", "Reese Jordan",
    "Quinn Blair", "Logan Hayes", "Rowan Brooks", "Emerson Lane",
    "Finley Wells", "Harper Parker", "Sage James", "Dakota Morgan",
    "Peyton Taylor", "Charlie Blair", "Jules Ellis", "Micah Gray",
    "Tatum Hart", "Elliot Knox", "Blair Monroe", "Shiloh Flynn",
    "Lennon Rivers", "Remy West", "Kendall Bennett", "Phoenix Ford",
    "Sawyer Kelly", "River Marsh", "Frankie Ramsey", "Marley Dean",
    "Noel Burke", "Justice Chandler", "Oakley Frost",
    "Ellis Bell", "Spencer Sloan", "Quincy Lowell", "Aubrey Vaughn",
    "Devon Jennings", "Rory Hale", "Shay Pierce", "Toby Tate",
    "Jesse Jordan", "Cory Cole", "Emery Drew", "Blake Shaw",
    "Casey Miles", "Taylor Bennett", "Jamie Douglas", "Morgan Grant"
]

def generate_email(name: str) -> str:
    """Generate email address from name."""
    return f"{name.lower().replace(' ', '.')}@email.com"


def get_random_attendees(count: int) -> list[tuple[str, str]]:
    """
    Get a list of random attendees (name, email) tuples.
    
    Args:
        count: Number of attendees to generate
        
    Returns:
        List of (name, email) tuples
    """
    import random
    
    # Sample without replacement to avoid duplicates
    selected_names = random.sample(SAMPLE_NAMES, min(count, len(SAMPLE_NAMES)))
    
    return [(name, generate_email(name)) for name in selected_names]