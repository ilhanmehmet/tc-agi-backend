from tavily import TavilyClient
import os

class WebSearcher:
    def __init__(self):
        self.api_key = os.environ.get("TAVILY_API_KEY", "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")
        self.client = TavilyClient(api_key=self.api_key)
        print("✅ Web searcher ready!")
    
    def search(self, query: str, max_results: int = 3):
        """Search web and return results"""
        try:
            response = self.client.search(query, max_results=max_results)
            results = []
            for result in response.get('results', []):
                results.append({
                    "title": result.get("title", ""),
                    "content": result.get("content", ""),
                    "url": result.get("url", "")
                })
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []

# Global instance
web_searcher = WebSearcher()
