from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class SeniorityEnum(str, Enum):
    JUNIOR = "JUNIOR"
    PLENO = "PLENO"
    SENIOR = "SENIOR"

class Education(BaseModel):
    institution: str = Field(description="Nome da instituição")
    degree: str = Field(description="Grau (Bacharelado, Tecnólogo, Pós, etc)")
    field: str = Field(description="Área de estudo")

class CandidateAnalysis(BaseModel):
    full_name: str = Field(description="Nome completo do candidato")
    email: Optional[str] = Field(None, description="E-mail de contato")
    phone: Optional[str] = Field(None, description="Telefone de contato")
    years_of_experience: float = Field(description="Anos totais de experiência")
    skills: List[str] = Field(description="Lista de habilidades técnicas")
    last_role: Optional[str] = Field(None, description="Último cargo ocupado")
    companies: List[str] = Field(description="Lista de empresas anteriores")
    education: List[Education] = Field(default_factory=list, description="Formação acadêmica")
    seniority: SeniorityEnum = Field(description="Senioridade estimada baseada na experiência")
    summary: str = Field(description="Breve resumo do perfil do candidato")
    strengths: List[str] = Field(description="Pontos fortes do candidato")
    weaknesses: List[str] = Field(description="Pontos a desenvolver ou faltantes para a vaga")
    
    # Internal usage for ranking
    match_score: float = Field(0.0, description="Pontuação de match com a vaga (0-100)")
    ranking_justification: str = Field("", description="Justificativa para a pontuação")

class RankedCandidate(BaseModel):
    rank: int
    candidate: CandidateAnalysis
    score: float

class ConsolidatedReport(BaseModel):
    job_description: str
    total_candidates: int
    ranking: List[RankedCandidate]
    recommendation: str = Field(description="Recomendação final de quais candidatos entrevistar")

class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

class TaskStatus(BaseModel):
    task_id: str
    status: str
    result: Optional[ConsolidatedReport] = None
