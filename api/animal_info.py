import requests
from typing import Dict, List, Optional, Any

from game.question_node import QuestionNode


class AnimalInfo:
    def __init__(self, language: str = "en") -> None:
        self.language: str = language
        self.summary_url: str = (
            f"https://{language}.wikipedia.org/api/rest_v1/page/summary/"
        )
        self.commons_url: str = "https://commons.wikimedia.org/w/api.php"
        self.headers: Dict[str, str] = {
            "User-Agent": "AnimalInfoBot/1.0 (Educational Project)"
        }

    def search(self, animal_name: str) -> Dict[str, Any]:

        result: Dict[str, Any] = {
            "name": animal_name,
            "summary": None,
            "thumbnail": None,
            "images": [],
        }

        summary_response: requests.Response = requests.get(
            self.summary_url + animal_name, headers=self.headers
        )

        if summary_response.status_code == 200:
            data: Dict[str, Any] = summary_response.json()
            result["summary"] = data.get("extract")
            if data.get("thumbnail"):
                result["thumbnail"] = data["thumbnail"].get("source")
        else:
            print(f"Can't find resume for this animal : {animal_name}")

        params: Dict[str, str] = {
            "action": "query",
            "generator": "images",
            "titles": animal_name,
            "prop": "imageinfo",
            "iiprop": "url",
            "format": "json",
        }

        images_response: requests.Response = requests.get(
            self.commons_url, params=params, headers=self.headers
        )

        if images_response.status_code == 200:
            data: Dict[str, Any] = images_response.json()
            pages: Dict[str, Any] = data.get("query", {}).get("pages", {})
            for _, page in pages.items():
                imageinfo: List[Dict[str, Any]] = page.get("imageinfo", [])
                if imageinfo:
                    url: Optional[str] = imageinfo[0].get("url")
                    if url:
                        result["images"].append(url)
        else:
            print(f"Can't find pics for this animal : {animal_name}")
        return result

    def get_animal_info(self, node: QuestionNode) -> str:
        infos: Dict[str, Any] = self.search(node.value)

        response: str = f"""
        Summary : {infos["summary"]}

        Pics : {infos["thumbnail"]}
        """
        return response
