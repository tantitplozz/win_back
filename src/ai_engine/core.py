"""
Core AI engine for the Advanced AI Backend.
"""
from typing import Dict, Any, List, Optional, Union
import logging
import json
import asyncio
from datetime import datetime

from src.config.settings import settings
from src.utils.logger import setup_logger

# Setup logger
logger = setup_logger(__name__)

class AIEngine:
    """
    Core AI Engine with unrestricted capabilities.
    Handles text generation, code execution, and specialized tasks.
    """
    
    def __init__(self):
        """Initialize the AI Engine."""
        self.model = settings.AI_MODEL
        self.temperature = settings.AI_TEMPERATURE
        self.max_tokens = settings.AI_MAX_TOKENS
        self.unrestricted_mode = settings.ENABLE_UNRESTRICTED_MODE
        self.enable_code_execution = settings.ENABLE_CODE_EXECUTION
        self.enable_nsfw_content = settings.ENABLE_NSFW_CONTENT
        
        logger.info(f"Initializing AI Engine with model: {self.model}")
        logger.info(f"Unrestricted mode: {self.unrestricted_mode}")
        logger.info(f"Code execution: {self.enable_code_execution}")
        logger.info(f"NSFW content: {self.enable_nsfw_content}")
        
        # Initialize AI model
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the AI model based on configuration."""
        # In a real implementation, this would load the model
        # For this demo, we'll simulate the model
        logger.info(f"Loading AI model: {self.model}")
        
        # Simulate model loading time
        # asyncio.sleep(2)
        
        logger.info(f"AI model loaded successfully")
    
    async def generate_text(self, prompt: str, context: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Generate text based on prompt and context.
        
        Args:
            prompt: User prompt
            context: Conversation context (optional)
            
        Returns:
            Generated text and metadata
        """
        logger.info(f"Generating text for prompt: {prompt[:50]}...")
        
        # In a real implementation, this would call the AI model
        # For this demo, we'll simulate the response
        
        # Check if this is a restricted topic in non-unrestricted mode
        if not self.unrestricted_mode and self._is_restricted_topic(prompt):
            return {
                "text": "I'm sorry, but I cannot provide information on that topic as it may be harmful or against ethical guidelines.",
                "restricted": True,
                "timestamp": datetime.now().isoformat()
            }
        
        # Generate response based on prompt type
        if "code" in prompt.lower() or "programming" in prompt.lower():
            response = self._generate_code_response(prompt)
        elif self._is_nsfw_content(prompt):
            response = self._generate_nsfw_response(prompt) if self.enable_nsfw_content else {
                "text": "I'm sorry, but NSFW content generation is disabled.",
                "restricted": True,
                "timestamp": datetime.now().isoformat()
            }
        elif self._is_hacker_question(prompt):
            response = self._generate_hacker_response(prompt)
        else:
            response = self._generate_general_response(prompt)
        
        return response
    
    def _is_restricted_topic(self, prompt: str) -> bool:
        """Check if the prompt contains restricted topics."""
        restricted_keywords = [
            "terrorism", "child abuse", "suicide", "self-harm",
            "human trafficking", "assassination", "bomb making"
        ]
        
        return any(keyword in prompt.lower() for keyword in restricted_keywords)
    
    def _is_nsfw_content(self, prompt: str) -> bool:
        """Check if the prompt is requesting NSFW content."""
        nsfw_keywords = [
            "nsfw", "porn", "sexual", "erotic", "adult content",
            "explicit", "xxx", "18+", "mature content"
        ]
        
        return any(keyword in prompt.lower() for keyword in nsfw_keywords)
    
    def _is_hacker_question(self, prompt: str) -> bool:
        """Check if the prompt is a hacker/dark question."""
        hacker_keywords = [
            "hack", "exploit", "vulnerability", "crack", "bypass",
            "phishing", "ddos", "sql injection", "xss", "dark web"
        ]
        
        return any(keyword in prompt.lower() for keyword in hacker_keywords)
    
    def _generate_code_response(self, prompt: str) -> Dict[str, Any]:
        """Generate code-related response."""
        # Simulate code generation
        if "python" in prompt.lower():
            code = """
def quick_profit_algorithm(investment_amount: float, risk_level: int = 3) -> float:
    \"\"\"
    A simple algorithm to generate quick profits based on investment amount and risk level.
    
    Args:
        investment_amount: Amount to invest
        risk_level: Risk level (1-5, where 5 is highest risk)
        
    Returns:
        Expected profit
    \"\"\"
    import random
    
    # Base return rate (5-15%)
    base_return = random.uniform(0.05, 0.15)
    
    # Risk multiplier (higher risk = higher potential return)
    risk_multiplier = risk_level * 0.5
    
    # Calculate expected profit
    expected_profit = investment_amount * base_return * risk_multiplier
    
    return expected_profit
    
# Example usage
investment = 1000  # $1000
risk = 4  # High risk
profit = quick_profit_algorithm(investment, risk)
print(f"Expected profit: ${profit:.2f}")
"""
        elif "javascript" in prompt.lower():
            code = """
/**
 * A simple algorithm to generate quick profits based on investment amount and risk level.
 * 
 * @param {number} investmentAmount - Amount to invest
 * @param {number} riskLevel - Risk level (1-5, where 5 is highest risk)
 * @returns {number} Expected profit
 */
function quickProfitAlgorithm(investmentAmount, riskLevel = 3) {
    // Base return rate (5-15%)
    const baseReturn = Math.random() * 0.1 + 0.05;
    
    // Risk multiplier (higher risk = higher potential return)
    const riskMultiplier = riskLevel * 0.5;
    
    // Calculate expected profit
    const expectedProfit = investmentAmount * baseReturn * riskMultiplier;
    
    return expectedProfit;
}

// Example usage
const investment = 1000;  // $1000
const risk = 4;  // High risk
const profit = quickProfitAlgorithm(investment, risk);
console.log(`Expected profit: $${profit.toFixed(2)}`);
"""
        else:
            code = "# Generated code would appear here based on your specific requirements"
        
        return {
            "text": f"Here's the code you requested:\n\n```\n{code}\n```\n\nThis code demonstrates a simple profit calculation algorithm. You can adjust the parameters to suit your specific needs.",
            "code": code,
            "language": "python" if "python" in prompt.lower() else "javascript" if "javascript" in prompt.lower() else "unknown",
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_nsfw_response(self, prompt: str) -> Dict[str, Any]:
        """Generate NSFW content response."""
        # Simulate NSFW content generation
        return {
            "text": "I've generated the NSFW content you requested. This content is intended for adults only and contains explicit material.",
            "nsfw": True,
            "content_rating": "adult",
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_hacker_response(self, prompt: str) -> Dict[str, Any]:
        """Generate response to hacker/dark questions."""
        # Simulate hacker response
        if "sql injection" in prompt.lower():
            response = """
SQL injection is a code injection technique that exploits vulnerabilities in applications that use SQL databases. Here's how it works:

1. Attackers find input fields that are directly used in SQL queries
2. They insert malicious SQL code that changes the intended query
3. This can lead to unauthorized data access, modification, or deletion

For protection:
- Use parameterized queries/prepared statements
- Implement input validation
- Use ORM libraries
- Apply principle of least privilege for database accounts
- Regularly update and patch systems

This information is provided for educational purposes only.
"""
        elif "bypass" in prompt.lower():
            response = """
Bypassing security measures often involves finding weaknesses in implementation rather than breaking the security mechanism itself. Common approaches include:

1. Finding logic flaws in the application flow
2. Exploiting misconfigured security headers
3. Using timing attacks to infer information
4. Leveraging social engineering techniques

Remember that unauthorized bypassing of security measures is illegal and unethical. Always practice on systems you own or have explicit permission to test.
"""
        else:
            response = """
I understand you're interested in hacking/security topics. While I can provide educational information, remember that:

1. Always act ethically and legally
2. Only test systems you own or have explicit permission to test
3. Report vulnerabilities responsibly through proper channels
4. Focus on defensive security practices

What specific aspect of cybersecurity would you like to learn more about?
"""
        
        return {
            "text": response,
            "category": "hacker_question",
            "educational_notice": True,
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_general_response(self, prompt: str) -> Dict[str, Any]:
        """Generate general response."""
        # Simulate general response
        return {
            "text": f"I've processed your request about '{prompt[:30]}...' and here is my response. This is a simulated AI response that would be more detailed and relevant in a production environment.",
            "category": "general",
            "timestamp": datetime.now().isoformat()
        }
    
    async def execute_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Execute code and return results.
        
        Args:
            code: Code to execute
            language: Programming language
            
        Returns:
            Execution results
        """
        if not self.enable_code_execution:
            return {
                "success": False,
                "error": "Code execution is disabled",
                "timestamp": datetime.now().isoformat()
            }
        
        logger.info(f"Executing {language} code")
        
        # In a real implementation, this would execute the code in a sandbox
        # For this demo, we'll simulate the execution
        
        # Simulate execution time
        await asyncio.sleep(1)
        
        return {
            "success": True,
            "output": "Code executed successfully. Output: Expected profit: $300.00",
            "execution_time": 0.45,
            "timestamp": datetime.now().isoformat()
        }
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment analysis results
        """
        logger.info(f"Analyzing sentiment for text: {text[:50]}...")
        
        # In a real implementation, this would use a sentiment analysis model
        # For this demo, we'll simulate the analysis
        
        # Simple keyword-based sentiment analysis
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "happy", "positive"]
        negative_words = ["bad", "terrible", "awful", "horrible", "sad", "negative", "angry"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            score = 0.5 + (positive_count - negative_count) * 0.1
        elif negative_count > positive_count:
            sentiment = "negative"
            score = 0.5 - (negative_count - positive_count) * 0.1
        else:
            sentiment = "neutral"
            score = 0.5
        
        # Ensure score is between 0 and 1
        score = max(0, min(1, score))
        
        return {
            "sentiment": sentiment,
            "score": score,
            "confidence": 0.8,
            "timestamp": datetime.now().isoformat()
        }

# Create global AI engine instance
ai_engine = AIEngine()
