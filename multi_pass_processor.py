"""
Multi-pass refinement system for iterative text improvement
"""

from typing import Dict, List, Any, Tuple
import time
from dataclasses import dataclass
from agent_coordinator import AgentCoordinator

@dataclass
class RefinementPass:
    """Represents a single refinement pass"""
    pass_number: int
    input_text: str
    output_text: str
    improvements: List[Dict[str, Any]]
    quality_score: float
    processing_time: float
    convergence_metrics: Dict[str, float]

class MultiPassProcessor:
    """Handles multi-pass iterative text refinement"""
    
    def __init__(self, coordinator: AgentCoordinator, max_passes: int = 3):
        self.coordinator = coordinator
        self.max_passes = max_passes
        self.convergence_threshold = 0.05  # Stop if improvement < 5%
        self.min_quality_threshold = 0.85  # Stop if quality > 85%
        
    def process_with_multiple_passes(self, 
                                   text: str, 
                                   selected_agents: List[str] = None,
                                   user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process text through multiple refinement passes"""
        
        passes = []
        current_text = text
        previous_quality = 0.0
        total_start_time = time.time()
        
        print(f"🔄 Starting multi-pass processing (max {self.max_passes} passes)")
        
        for pass_num in range(1, self.max_passes + 1):
            print(f"   Pass {pass_num}: Processing...")
            pass_start_time = time.time()
            
            # Process current text
            results = self.coordinator.process_text(current_text, selected_agents)
            
            # Calculate metrics for this pass
            quality_score = results.get('final_validation', {}).get('quality_score', 0.0)
            processing_time = time.time() - pass_start_time
            
            # Create pass record
            current_pass = RefinementPass(
                pass_number=pass_num,
                input_text=current_text,
                output_text=results['corrected_text'],
                improvements=results.get('improvements', []),
                quality_score=quality_score,
                processing_time=processing_time,
                convergence_metrics=self._calculate_convergence_metrics(
                    current_text, results['corrected_text'], previous_quality, quality_score
                )
            )
            
            passes.append(current_pass)
            
            # Check convergence conditions
            should_continue, reason = self._should_continue_processing(
                current_pass, previous_quality, pass_num
            )
            
            print(f"   Pass {pass_num}: Quality {quality_score:.1%}, {len(current_pass.improvements)} improvements")
            
            if not should_continue:
                print(f"   🛑 Stopping: {reason}")
                break
            
            # Prepare for next pass
            current_text = results['corrected_text']
            previous_quality = quality_score
        
        total_time = time.time() - total_start_time
        
        # Compile final results
        final_results = self._compile_multi_pass_results(passes, total_time, user_preferences)
        
        print(f"✅ Multi-pass completed: {len(passes)} passes, {total_time:.1f}s")
        return final_results
    
    def _calculate_convergence_metrics(self, 
                                     input_text: str, 
                                     output_text: str, 
                                     prev_quality: float, 
                                     curr_quality: float) -> Dict[str, float]:
        """Calculate convergence metrics for this pass"""
        
        # Text similarity (simple character-based)
        if len(input_text) > 0:
            text_similarity = 1 - (abs(len(output_text) - len(input_text)) / len(input_text))
        else:
            text_similarity = 1.0
        
        # Quality improvement
        quality_improvement = curr_quality - prev_quality if prev_quality > 0 else curr_quality
        
        # Change ratio
        changes_made = input_text != output_text
        change_ratio = 0.0 if not changes_made else min(1.0, abs(len(output_text) - len(input_text)) / len(input_text))
        
        return {
            "text_similarity": text_similarity,
            "quality_improvement": quality_improvement,
            "change_ratio": change_ratio,
            "changes_made": changes_made
        }
    
    def _should_continue_processing(self, 
                                  current_pass: RefinementPass, 
                                  previous_quality: float, 
                                  pass_number: int) -> Tuple[bool, str]:
        """Determine if processing should continue"""
        
        # Check maximum passes
        if pass_number >= self.max_passes:
            return False, f"Maximum passes ({self.max_passes}) reached"
        
        # Check quality threshold
        if current_pass.quality_score >= self.min_quality_threshold:
            return False, f"Quality threshold reached ({current_pass.quality_score:.1%})"
        
        # Check convergence (minimal improvement)
        if pass_number > 1:
            improvement = current_pass.convergence_metrics.get("quality_improvement", 0)
            if improvement < self.convergence_threshold:
                return False, f"Convergence detected (improvement: {improvement:.1%})"
        
        # Check if no changes were made
        if not current_pass.convergence_metrics.get("changes_made", True):
            return False, "No changes made in this pass"
        
        return True, "Continue processing"
    
    def _compile_multi_pass_results(self, 
                                   passes: List[RefinementPass], 
                                   total_time: float,
                                   user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """Compile final results from all passes"""
        
        if not passes:
            return {"error": "No passes completed"}
        
        final_pass = passes[-1]
        initial_text = passes[0].input_text
        
        # Aggregate all improvements
        all_improvements = []
        for pass_obj in passes:
            for improvement in pass_obj.improvements:
                improvement["pass_number"] = pass_obj.pass_number
                all_improvements.append(improvement)
        
        # Calculate overall metrics
        overall_metrics = {
            "total_passes": len(passes),
            "total_time": total_time,
            "initial_quality": passes[0].quality_score,
            "final_quality": final_pass.quality_score,
            "quality_improvement": final_pass.quality_score - passes[0].quality_score,
            "total_improvements": len(all_improvements),
            "convergence_achieved": final_pass.quality_score >= self.min_quality_threshold
        }
        
        # Create pass summary
        pass_summary = []
        for pass_obj in passes:
            pass_summary.append({
                "pass": pass_obj.pass_number,
                "quality": pass_obj.quality_score,
                "improvements": len(pass_obj.improvements),
                "time": pass_obj.processing_time,
                "changes_made": pass_obj.convergence_metrics.get("changes_made", False)
            })
        
        return {
            "original_text": initial_text,
            "final_text": final_pass.output_text,
            "all_improvements": all_improvements,
            "overall_metrics": overall_metrics,
            "pass_summary": pass_summary,
            "passes_detail": passes,
            "processing_type": "multi_pass_refinement"
        }
    
    def get_optimization_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Get recommendations for further optimization"""
        recommendations = []
        
        metrics = results.get("overall_metrics", {})
        
        # Quality-based recommendations
        final_quality = metrics.get("final_quality", 0)
        if final_quality < 0.7:
            recommendations.append("Consider manual review - quality below 70%")
        elif final_quality < 0.85:
            recommendations.append("Good quality achieved - minor improvements possible")
        else:
            recommendations.append("Excellent quality achieved!")
        
        # Pass efficiency recommendations
        total_passes = metrics.get("total_passes", 0)
        if total_passes == 1:
            recommendations.append("Single pass was sufficient - text was already clear")
        elif total_passes >= self.max_passes:
            recommendations.append("Maximum passes used - consider manual refinement")
        
        # Improvement distribution
        improvement_count = metrics.get("total_improvements", 0)
        if improvement_count == 0:
            recommendations.append("No automatic improvements made - text may already be optimal")
        elif improvement_count > 10:
            recommendations.append("Many improvements applied - verify meaning preservation")
        
        return recommendations

class AdvancedProcessingOptions:
    """Advanced processing options and user preferences"""
    
    def __init__(self):
        self.processing_modes = {
            "conservative": {
                "max_passes": 2,
                "convergence_threshold": 0.10,
                "min_quality_threshold": 0.75,
                "description": "Minimal changes, preserve original style"
            },
            "balanced": {
                "max_passes": 3,
                "convergence_threshold": 0.05,
                "min_quality_threshold": 0.85,
                "description": "Balanced improvement with reasonable changes"
            },
            "aggressive": {
                "max_passes": 5,
                "convergence_threshold": 0.02,
                "min_quality_threshold": 0.95,
                "description": "Maximum clarity, extensive improvements"
            }
        }
    
    def get_processing_config(self, mode: str) -> Dict[str, Any]:
        """Get configuration for processing mode"""
        return self.processing_modes.get(mode, self.processing_modes["balanced"])
    
    def create_custom_processor(self, 
                              coordinator: AgentCoordinator, 
                              mode: str = "balanced") -> MultiPassProcessor:
        """Create processor with specific mode configuration"""
        config = self.get_processing_config(mode)
        
        processor = MultiPassProcessor(coordinator, max_passes=config["max_passes"])
        processor.convergence_threshold = config["convergence_threshold"]
        processor.min_quality_threshold = config["min_quality_threshold"]
        
        return processor