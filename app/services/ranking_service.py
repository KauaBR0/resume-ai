from typing import List
from app.models.schemas import CandidateAnalysis, RankedCandidate

def rank_candidates(candidates: List[CandidateAnalysis]) -> List[RankedCandidate]:
    """
    Ranks candidates based on their match_score.
    """
    # Sort by score descending
    sorted_candidates = sorted(candidates, key=lambda c: c.match_score, reverse=True)
    
    ranked_list = []
    for index, candidate in enumerate(sorted_candidates, 1):
        ranked_list.append(
            RankedCandidate(
                rank=index,
                candidate=candidate,
                score=candidate.match_score
            )
        )
    
    return ranked_list
