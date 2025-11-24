"""Training service for interactive learning modules on AI infrastructure economics."""
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class TrainingService:
    """Interactive training service for AI infrastructure analysis.

    Provides structured learning modules for:
    - GPU architecture and economics
    - Datacenter TCO modeling
    - Neocloud financial analysis
    - Bloomberg data integration
    """

    def __init__(self):
        """Initialize training service."""
        self.modules = self._initialize_modules()
        self.user_progress = {}

    def _initialize_modules(self) -> Dict[str, Any]:
        """Initialize training modules."""
        return {
            "gpu_fundamentals": {
                "title": "GPU Architecture Fundamentals",
                "description": "Learn about GPU architectures for AI/ML workloads",
                "lessons": [
                    {
                        "id": "gpu_1",
                        "title": "Introduction to AI GPUs",
                        "content": """
# Introduction to AI GPUs

Modern AI training and inference rely heavily on specialized GPU hardware.

## Key Concepts

**1. GPU vs CPU for AI**
- GPUs excel at parallel processing
- Thousands of cores vs dozens in CPUs
- Optimized for matrix operations

**2. Key Specifications**
- **TFLOPS**: Trillion floating-point operations per second
- **Memory Bandwidth**: GB/s data transfer rate
- **TDP**: Thermal Design Power in watts

**3. Major Players**
- NVIDIA: H100, H200, B200 (Blackwell)
- AMD: MI300X
- Intel: Gaudi series
""",
                        "quiz": [
                            {
                                "question": "Why are GPUs better than CPUs for AI training?",
                                "options": [
                                    "Higher clock speed",
                                    "Massive parallelism for matrix operations",
                                    "Lower power consumption",
                                    "Simpler programming model"
                                ],
                                "correct": 1,
                                "explanation": "GPUs have thousands of cores optimized for parallel matrix operations, which are fundamental to neural network computations."
                            },
                            {
                                "question": "What does TFLOPS measure?",
                                "options": [
                                    "Memory capacity",
                                    "Power consumption",
                                    "Floating-point operations per second",
                                    "Data transfer speed"
                                ],
                                "correct": 2,
                                "explanation": "TFLOPS (Trillion FLOPS) measures computational throughput - how many floating-point operations the GPU can perform per second."
                            }
                        ]
                    },
                    {
                        "id": "gpu_2",
                        "title": "NVIDIA Datacenter GPUs",
                        "content": """
# NVIDIA Datacenter GPU Evolution

## Architecture Generations

**1. Ampere (A100)**
- 7nm process
- 80GB HBM2e
- 312 TFLOPS FP16

**2. Hopper (H100/H200)**
- 4nm process
- 80-141GB HBM3/HBM3e
- 1,979 TFLOPS FP16
- Transformer Engine

**3. Blackwell (B100/B200)**
- 4nm process
- 192GB HBM3e
- ~4,500 TFLOPS FP16
- Second-gen Transformer Engine

## Key Innovations
- NVLink for multi-GPU communication
- HBM (High Bandwidth Memory)
- Tensor Cores for AI operations
""",
                        "quiz": [
                            {
                                "question": "Which architecture introduced the Transformer Engine?",
                                "options": ["Ampere", "Hopper", "Blackwell", "Volta"],
                                "correct": 1,
                                "explanation": "The Transformer Engine was introduced with the Hopper architecture (H100), providing optimized performance for transformer-based models."
                            }
                        ]
                    }
                ]
            },
            "tco_modeling": {
                "title": "TCO Modeling for GPU Infrastructure",
                "description": "Master total cost of ownership calculations",
                "lessons": [
                    {
                        "id": "tco_1",
                        "title": "TCO Components",
                        "content": """
# Total Cost of Ownership Components

## Capital Expenditure (CapEx)

**Hardware Costs:**
- GPUs: $15,000 - $40,000 each
- Servers: $5,000 - $15,000
- Networking: $500 - $2,000 per GPU
- Storage: Variable

## Operating Expenditure (OpEx)

**1. Power Costs**
```
Annual Power = TDP × Hours × PUE / 1000 × Rate

Example (H100):
= 700W × 8,760h × 1.3 / 1000 × $0.08/kWh
= $6,370 per GPU per year
```

**2. Cooling (included in PUE)**
- PUE 1.2 = 20% cooling overhead
- PUE 1.5 = 50% cooling overhead

**3. Maintenance**
- Typically 5-10% of CapEx annually

**4. Personnel**
- Often overlooked but significant
""",
                        "quiz": [
                            {
                                "question": "What does PUE stand for?",
                                "options": [
                                    "Power Unit Efficiency",
                                    "Power Usage Effectiveness",
                                    "Processing Unit Energy",
                                    "Parallel Utilization Efficiency"
                                ],
                                "correct": 1,
                                "explanation": "PUE (Power Usage Effectiveness) measures datacenter efficiency - total facility power divided by IT equipment power. A PUE of 1.3 means 30% overhead."
                            },
                            {
                                "question": "If an H100 has 700W TDP and runs 24/7, what's the annual kWh consumption?",
                                "options": ["5,000 kWh", "6,132 kWh", "8,760 kWh", "10,000 kWh"],
                                "correct": 1,
                                "explanation": "700W × 8,760 hours = 6,132 kWh per year (not including PUE overhead)"
                            }
                        ]
                    },
                    {
                        "id": "tco_2",
                        "title": "Build vs Buy Analysis",
                        "content": """
# Build vs Buy: On-Premise vs Cloud

## On-Premise Advantages
- Lower long-term costs at high utilization
- Full control over hardware
- Data sovereignty
- Predictable costs

## Cloud Advantages
- No upfront capital
- Scalability
- Latest hardware access
- Geographic distribution

## Break-Even Analysis

**Key Variables:**
- Utilization rate
- Time horizon
- Cloud pricing
- Capital cost of equipment

**Rule of Thumb:**
- <50% utilization: Cloud usually wins
- >70% utilization: On-premise usually wins
- 50-70%: Detailed analysis needed
""",
                        "quiz": [
                            {
                                "question": "At what utilization rate does on-premise typically become more cost-effective?",
                                "options": ["20-30%", "40-50%", "70%+", "90%+"],
                                "correct": 2,
                                "explanation": "Generally, on-premise infrastructure becomes more cost-effective above 70% utilization, when the fixed costs are spread across substantial usage."
                            }
                        ]
                    }
                ]
            },
            "neocloud_economics": {
                "title": "Neocloud Provider Economics",
                "description": "Analyze GPU cloud provider business models",
                "lessons": [
                    {
                        "id": "neo_1",
                        "title": "Neocloud Business Models",
                        "content": """
# Neocloud Provider Economics

## What are Neoclouds?
Specialized cloud providers focused on GPU/AI infrastructure, distinct from hyperscalers.

## Key Players
- **CoreWeave**: Kubernetes-native GPU cloud
- **Lambda Labs**: Developer-focused ML cloud
- **Together AI**: Inference optimization
- **Crusoe**: Sustainable/stranded energy focus

## Business Model Components

**1. Infrastructure Costs**
- GPU procurement (often with NVIDIA allocation)
- Datacenter capacity
- Networking

**2. Revenue Streams**
- On-demand GPU hours
- Reserved capacity
- Managed services

**3. Unit Economics**
```
Gross Margin = (Hourly Rate - Hourly Cost) / Hourly Rate

Example:
Selling H100 at $3.50/hr
Cost: $1.50/hr (including depreciation, power, ops)
Gross Margin = 57%
```
""",
                        "quiz": [
                            {
                                "question": "What differentiates neoclouds from hyperscalers?",
                                "options": [
                                    "Lower prices",
                                    "GPU/AI infrastructure specialization",
                                    "More datacenters",
                                    "Better customer support"
                                ],
                                "correct": 1,
                                "explanation": "Neoclouds specialize in GPU/AI infrastructure, offering purpose-built solutions rather than general-purpose cloud services."
                            }
                        ]
                    }
                ]
            },
            "bloomberg_integration": {
                "title": "Bloomberg Terminal Integration",
                "description": "Learn to integrate Bloomberg data feeds",
                "lessons": [
                    {
                        "id": "bbg_1",
                        "title": "Bloomberg API Overview",
                        "content": """
# Bloomberg API Integration

## API Options

**1. Desktop API (DAPI)**
- Connects to running Terminal
- localhost:8194
- Requires Terminal subscription

**2. Server API (B-PIPE)**
- Server-side integration
- No Terminal required
- Enterprise licensing

## Key Services

**Reference Data (//blp/refdata)**
- Current prices
- Company fundamentals
- Historical data

**Market Data (//blp/mktdata)**
- Real-time quotes
- Live updates

## Python Integration

```python
import blpapi

# Connect to Terminal
options = blpapi.SessionOptions()
options.setServerHost('localhost')
options.setServerPort(8194)

session = blpapi.Session(options)
session.start()
session.openService("//blp/refdata")
```
""",
                        "quiz": [
                            {
                                "question": "What port does Bloomberg Desktop API use?",
                                "options": ["8080", "8194", "443", "3000"],
                                "correct": 1,
                                "explanation": "Bloomberg Desktop API listens on port 8194 by default."
                            }
                        ]
                    }
                ]
            }
        }

    def get_modules(self) -> List[Dict[str, Any]]:
        """Get list of available training modules."""
        return [
            {
                "id": module_id,
                "title": module["title"],
                "description": module["description"],
                "lesson_count": len(module["lessons"])
            }
            for module_id, module in self.modules.items()
        ]

    def get_module(self, module_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific training module."""
        return self.modules.get(module_id)

    def get_lesson(self, module_id: str, lesson_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific lesson from a module."""
        module = self.modules.get(module_id)
        if not module:
            return None

        for lesson in module["lessons"]:
            if lesson["id"] == lesson_id:
                return lesson
        return None

    def submit_quiz(self, module_id: str, lesson_id: str,
                   answers: List[int], user_id: str = "default") -> Dict[str, Any]:
        """Submit quiz answers and get results.

        Args:
            module_id: Module identifier
            lesson_id: Lesson identifier
            answers: List of answer indices
            user_id: User identifier for tracking progress

        Returns:
            Quiz results with score and explanations
        """
        lesson = self.get_lesson(module_id, lesson_id)
        if not lesson:
            return {"error": "Lesson not found"}

        quiz = lesson.get("quiz", [])
        if len(answers) != len(quiz):
            return {"error": "Answer count mismatch"}

        results = []
        correct_count = 0

        for i, (answer, question) in enumerate(zip(answers, quiz)):
            is_correct = answer == question["correct"]
            if is_correct:
                correct_count += 1

            results.append({
                "question": question["question"],
                "your_answer": question["options"][answer] if 0 <= answer < len(question["options"]) else "Invalid",
                "correct_answer": question["options"][question["correct"]],
                "is_correct": is_correct,
                "explanation": question["explanation"]
            })

        score = (correct_count / len(quiz)) * 100 if quiz else 0

        # Update user progress
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {}
        self.user_progress[user_id][f"{module_id}_{lesson_id}"] = {
            "score": score,
            "completed": True
        }

        return {
            "score": score,
            "correct": correct_count,
            "total": len(quiz),
            "results": results,
            "passed": score >= 70
        }

    def get_user_progress(self, user_id: str = "default") -> Dict[str, Any]:
        """Get user's learning progress."""
        progress = self.user_progress.get(user_id, {})

        total_lessons = sum(len(m["lessons"]) for m in self.modules.values())
        completed_lessons = len(progress)
        avg_score = sum(p["score"] for p in progress.values()) / len(progress) if progress else 0

        return {
            "user_id": user_id,
            "completed_lessons": completed_lessons,
            "total_lessons": total_lessons,
            "completion_percent": (completed_lessons / total_lessons) * 100 if total_lessons else 0,
            "average_score": avg_score,
            "lesson_details": progress
        }
