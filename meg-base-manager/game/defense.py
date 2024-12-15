from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random

@dataclass
class DefenseStructure:
    name: str
    level: int = 1
    defense_bonus: int = 0     # Bonus difesa base
    research_bonus: int = 0    # Bonus alla ricerca
    medical_bonus: int = 0     # Bonus alle cure
    morale_bonus: int = 0      # Bonus al morale
    diplomatic_bonus: int = 0  # Bonus diplomatici
    survival_bonus: int = 0    # Bonus sopravvivenza
    resource_cost: Dict[str, int] = field(default_factory=dict)
    specialist_bonus: Dict[str, float] = field(default_factory=dict)  # Bonus basati sulle specializzazioni
    daily_production: Dict[str, int] = field(default_factory=dict)  # Risorse prodotte ogni giorno
    
class DefenseSystem:
    def __init__(self):
        self.alert_level: int = 1  # Da 1 a 5
        self.defense_rating: int = 10
        self.structures: List[DefenseStructure] = []
        self.research_progress: float = 0.0  # Progresso verso il prossimo punto intel
        
        # Strutture disponibili
        self.available_structures = {
            # Strutture di Base
            "radio_tower": DefenseStructure(
                "Torre Radio",
                1,
                defense_bonus=2,
                diplomatic_bonus=5,
                morale_bonus=3,
                resource_cost={"supplies": 30, "fuel": 20},
                specialist_bonus={"diplomat": 1.2, "engineer": 1.1},
                daily_production={"supplies": 2}  # Attrae sopravvissuti che portano rifornimenti
            ),
            "walls": DefenseStructure(
                "Mura Rinforzate",
                1,
                defense_bonus=5,
                survival_bonus=2,
                resource_cost={"supplies": 20},
                specialist_bonus={"combat_specialist": 1.2, "engineer": 1.1},
                daily_production={"almond_water": 1}  # Raccolta acqua piovana
            ),
            "turrets": DefenseStructure(
                "Torrette Difensive",
                1,
                defense_bonus=7,
                resource_cost={"supplies": 25, "fuel": 15},
                specialist_bonus={"combat_specialist": 1.3, "engineer": 1.2},
                daily_production={"supplies": 1}  # Raccolta risorse da entità eliminate
            ),
            
            # Strutture di Monitoraggio
            "sensors": DefenseStructure(
                "Sensori di Movimento",
                1,
                defense_bonus=3,
                research_bonus=2,
                resource_cost={"fuel": 10, "supplies": 15},
                specialist_bonus={"engineer": 1.2, "scout": 1.1}
            ),
            "monitoring": DefenseStructure(
                "Centro di Monitoraggio",
                1,
                defense_bonus=2,
                research_bonus=5,
                resource_cost={"supplies": 30, "fuel": 20},
                specialist_bonus={"researcher": 1.3}
            ),
            
            # Strutture Mediche
            "infirmary": DefenseStructure(
                "Infermeria",
                1,
                medical_bonus=5,
                morale_bonus=2,
                resource_cost={"medical": 25, "supplies": 15},
                specialist_bonus={"medic": 1.4}
            ),
            "psych_ward": DefenseStructure(
                "Centro Psicologico",
                1,
                medical_bonus=2,
                morale_bonus=5,
                resource_cost={"medical": 15, "supplies": 10},
                specialist_bonus={"psychologist": 1.3}
            ),
            
            # Strutture di Sopravvivenza
            "greenhouse": DefenseStructure(
                "Serra Idroponica",
                1,
                survival_bonus=4,
                resource_cost={"supplies": 30, "almond_water": 20},
                specialist_bonus={"survivalist": 1.3}
            ),
            "water_purifier": DefenseStructure(
                "Purificatore d'Acqua",
                1,
                survival_bonus=5,
                resource_cost={"supplies": 25, "fuel": 15},
                specialist_bonus={"engineer": 1.2, "survivalist": 1.2}
            ),
            
            # Strutture Diplomatiche
            "embassy": DefenseStructure(
                "Ambasciata",
                1,
                diplomatic_bonus=10,
                morale_bonus=5,
                resource_cost={"supplies": 50, "medical": 20, "almond_water": 25},
                specialist_bonus={"diplomat": 2.0, "psychologist": 1.5}
            ),
            "comm_center": DefenseStructure(
                "Centro Comunicazioni",
                1,
                diplomatic_bonus=5,
                morale_bonus=2,
                resource_cost={"supplies": 20, "fuel": 15},
                specialist_bonus={"diplomat": 1.4}
            ),
            "meeting_hall": DefenseStructure(
                "Sala Riunioni",
                1,
                diplomatic_bonus=3,
                morale_bonus=3,
                resource_cost={"supplies": 15},
                specialist_bonus={"diplomat": 1.2, "psychologist": 1.1}
            ),
            
            # Strutture di Ricerca
            "research_lab": DefenseStructure(
                "Laboratorio di Ricerca",
                1,
                research_bonus=7,
                resource_cost={"supplies": 35, "fuel": 20},
                specialist_bonus={"researcher": 1.5}
            ),
            "archive": DefenseStructure(
                "Archivio Dati",
                1,
                research_bonus=4,
                resource_cost={"supplies": 20},
                specialist_bonus={"researcher": 1.2, "explorer": 1.1}
            )
        }
        
    def increase_alert(self):
        if self.alert_level < 5:
            self.alert_level += 1
            
    def decrease_alert(self):
        if self.alert_level > 1:
            self.alert_level -= 1
            
    def get_total_defense(self) -> int:
        base_defense = self.defense_rating
        structure_bonus = sum(s.defense_bonus for s in self.structures)
        alert_bonus = self.alert_level * 2
        return base_defense + structure_bonus + alert_bonus
        
    def get_research_bonus(self, personnel) -> int:
        """Calcola il bonus totale alla ricerca considerando le strutture e le specializzazioni"""
        base_bonus = sum(s.research_bonus for s in self.structures)
        specialist_bonus = 0
        for structure in self.structures:
            if structure.specialist_bonus:
                for agent in personnel.agents:
                    if agent.role.lower() in structure.specialist_bonus:
                        specialist_bonus += structure.research_bonus * (structure.specialist_bonus[agent.role.lower()] - 1)
        return base_bonus + int(specialist_bonus)
        
    def get_medical_bonus(self, personnel) -> int:
        """Calcola il bonus medico totale"""
        base_bonus = sum(s.medical_bonus for s in self.structures)
        specialist_bonus = 0
        for structure in self.structures:
            if structure.specialist_bonus:
                for agent in personnel.agents:
                    if agent.role.lower() in structure.specialist_bonus:
                        specialist_bonus += structure.medical_bonus * (structure.specialist_bonus[agent.role.lower()] - 1)
        return base_bonus + int(specialist_bonus)
        
    def get_diplomatic_bonus(self, personnel) -> int:
        """Calcola il bonus diplomatico totale"""
        base_bonus = sum(s.diplomatic_bonus for s in self.structures)
        specialist_bonus = 0
        for structure in self.structures:
            if structure.specialist_bonus:
                for agent in personnel.agents:
                    if agent.role.lower() in structure.specialist_bonus:
                        specialist_bonus += structure.diplomatic_bonus * (structure.specialist_bonus[agent.role.lower()] - 1)
        return base_bonus + int(specialist_bonus)
        
    def get_survival_bonus(self, personnel) -> int:
        """Calcola il bonus alla sopravvivenza totale"""
        base_bonus = sum(s.survival_bonus for s in self.structures)
        specialist_bonus = 0
        for structure in self.structures:
            if structure.specialist_bonus:
                for agent in personnel.agents:
                    if agent.role.lower() in structure.specialist_bonus:
                        specialist_bonus += structure.survival_bonus * (structure.specialist_bonus[agent.role.lower()] - 1)
        return base_bonus + int(specialist_bonus)
        
    def get_morale_bonus(self, personnel) -> int:
        """Calcola il bonus al morale totale"""
        base_bonus = sum(s.morale_bonus for s in self.structures)
        specialist_bonus = 0
        for structure in self.structures:
            if structure.specialist_bonus:
                for agent in personnel.agents:
                    if agent.role.lower() in structure.specialist_bonus:
                        specialist_bonus += structure.morale_bonus * (structure.specialist_bonus[agent.role.lower()] - 1)
        return base_bonus + int(specialist_bonus)
        
    def get_structure_by_number(self, number: int) -> Optional[DefenseStructure]:
        """Ottieni una struttura dal suo numero (1-based)"""
        structures = list(self.available_structures.values())
        if number < 1 or number > len(structures):
            return None
        return structures[number - 1]
        
    def build_structure(self, struct_number: int, game_state) -> bool:
        structure = self.get_structure_by_number(struct_number)
        if not structure:
            return False
        
        # Verifica risorse
        for resource, amount in structure.resource_cost.items():
            if game_state.resources.get(resource) < amount:
                return False
                
        # Consuma risorse
        for resource, amount in structure.resource_cost.items():
            game_state.resources.modify(resource, -amount)
            
        self.structures.append(structure)
        self.defense_rating += structure.defense_bonus
        return True
        
    def to_dict(self) -> Dict:
        return {
            "alert_level": self.alert_level,
            "defense_rating": self.defense_rating,
            "structures": [
                {
                    "name": s.name,
                    "level": s.level,
                    "defense_bonus": s.defense_bonus
                }
                for s in self.structures
            ]
        }
        
    def from_dict(self, data: Dict):
        self.alert_level = data["alert_level"]
        self.defense_rating = data["defense_rating"]
        self.structures = [
            DefenseStructure(
                s["name"],
                s["level"],
                s["defense_bonus"],
                {}  # I costi non sono necessari per strutture già costruite
            )
            for s in data["structures"]
        ]
        
    def reset(self):
        self.__init__()
    def daily_update(self, game_state):
        """Aggiorna il progresso della ricerca, genera intel points e gestisce produzione"""
        # Gestione ricerca
        research_power = sum(s.research_bonus for s in self.structures)
        if research_power > 0:
            self.research_progress += research_power * 0.1
            while self.research_progress >= 10:
                self.research_progress -= 10
                game_state.intel.add_intel_points("level_0", 5, "Ricerca")
                
        # Produzione giornaliera delle strutture
        for structure in self.structures:
            for resource, amount in structure.daily_production.items():
                game_state.resources.modify(resource, amount)
                
        # Sistema di infiltrazione
        if random.random() < 0.1:  # 10% di chance giornaliera di infiltrazione
            infiltration_defense = self.get_total_defense()
            if random.randint(1, 100) > infiltration_defense:
                # Infiltrazione riuscita
                damage = random.randint(1, 3)
                target = random.choice(["resources", "morale", "intel"])
                
                if target == "resources":
                    resource = random.choice(list(game_state.resources.resources.keys()))
                    amount = random.randint(5, 15)
                    game_state.resources.modify(resource, -amount)
                    game_state.events.trigger_event(Event(
                        "infiltration",
                        "Infiltrazione",
                        f"Agenti ostili hanno rubato {amount} unità di {resource}",
                        {"resources": {resource: -amount}}
                    ), game_state)
                elif target == "morale":
                    game_state.stats.morale = max(0, game_state.stats.morale - damage * 5)
                    game_state.events.trigger_event(Event(
                        "infiltration",
                        "Infiltrazione",
                        "Agenti ostili hanno danneggiato il morale della base",
                        {"stats": {"morale": -damage * 5}}
                    ), game_state)
                else:
                    # Perdita di intel points
                    game_state.intel.add_intel_points("level_0", -damage * 5, "Infiltrazione")