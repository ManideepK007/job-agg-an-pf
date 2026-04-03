def calculate_match_score(user_skills, job_skills):
    """
    Uses Set Intersection to find the percentage of skills matched.
    Time Complexity: O(n) where n is the number of skills.
    """
    if not job_skills:
        return 0
    
    # Convert lists of objects to sets of skill names/IDs
    u_set = set(s.id for s in user_skills)
    j_set = set(s.id for s in job_skills)
    
    # Find common skills
    common = u_set.intersection(j_set)
    
    score = (len(common) / len(j_set)) * 100
    return round(score, 2)