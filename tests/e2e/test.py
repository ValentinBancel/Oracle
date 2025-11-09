from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import List, Optional

class Test_E2E():
    def __init__(self, base_url: str = "http://localhost:8501", username: str = "TestUser") -> None:
        self.driver = None
        self.base_url: str = base_url
        self.wait_timeout: int = 10
        self.username: str = username

    def _init_driver(self) -> webdriver.Chrome:
        """
        Initialize and configure a Selenium WebDriver instance.
        Returns:
            WebDriver: A configured Selenium WebDriver instance ready for web scraping.
        Raises:
            Exception: If there's an error during driver initialization.
        """
        try:
            options = Options()
            options.add_argument("--incognito")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--headless")

            driver = webdriver.Chrome(options=options)
            
            return driver
        except Exception as e:
            raise e
    
    def _wait_for_streamlit_ready(self) -> None:
        """Wait for Streamlit app to be fully loaded."""
        WebDriverWait(self.driver, self.wait_timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(2)  

    def _login(self) -> bool:
        """
        Handle the login process by entering username and clicking Start Playing.
        
        Returns:
            True if login was successful, False otherwise
        """
        try:
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            if "enter your username" in body_text.lower():
                print(f"Logging in with username: {self.username}")
                
                # Find and fill the username input
                if not self._fill_input("Enter your username", self.username):
                    print("Failed to enter username")
                    return False
                
                # Click Start Playing button
                if not self._click_button("Start Playing"):
                    print("Failed to click 'Start Playing' button")
                    return False
                
                time.sleep(2)  # Wait for app to initialize after login
                print(f"✓ Successfully logged in as {self.username}")
                return True
            else:
                print("Already logged in or login screen not detected")
                return True
                
        except Exception as e:
            print(f"Error during login: {e}")
            return False
    
    def _click_button(self, button_text: str) -> bool:
        """
        Permit to bot click on a button identified by its text content.
        
        Args:
            button_text: The text content of the button to click
            
        Returns:
            True if button was found and clicked, False otherwise
        """
        try:
            # Streamlit buttons are usually within a div with data-testid="stButton"
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            
            for button in buttons:
                if button_text.lower() in button.text.lower():
                    button.click()
                    time.sleep(1)  # Wait for UI to update
                    return True
            
            print(f"Button with text '{button_text}' not found")
            return False
        except Exception as e:
            print(f"Error clicking button '{button_text}': {e}")
            return False
    
    def _get_current_question(self) -> Optional[str]:
        """
        Returns:
            The question text or None if not found
        """
        try:
            elements = self.driver.find_elements(By.CLASS_NAME, "big-font")
            if elements:
                return elements[0].text

            headers = self.driver.find_elements(By.TAG_NAME, "h2")
            headers.extend(self.driver.find_elements(By.TAG_NAME, "h3"))
            
            for header in headers:
                text = header.text.strip()
                if text and "?" in text:
                    return text
            
            return None
        except Exception as e:
            print(f"Error getting current question: {e}")
            return None
    
    def _get_score_info(self) -> dict:
        """
        Get the current score information from the sidebar.
        
        Returns:
            Dictionary with 'session_score' and 'total_score' keys
        """
        try:
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            # Look for score information in the sidebar
            score_info = {
                "session_score": 0,
                "total_score": 0,
                "questions_asked": 0
            }
            
            # Parse the text to find scores
            lines = body_text.split('\n')
            for i, line in enumerate(lines):
                if "Session Score" in line and i + 1 < len(lines):
                    try:
                        score_info["session_score"] = int(lines[i + 1])
                    except ValueError:
                        pass
                elif "Total Score" in line and i + 1 < len(lines):
                    try:
                        score_info["total_score"] = int(lines[i + 1])
                    except ValueError:
                        pass
                elif "Questions Asked" in line and i + 1 < len(lines):
                    try:
                        score_info["questions_asked"] = int(lines[i + 1])
                    except ValueError:
                        pass
            
            return score_info
        except Exception as e:
            print(f"Error getting score info: {e}")
            return {"session_score": 0, "total_score": 0, "questions_asked": 0}
    
    def _fill_input(self, placeholder: str, value: str) -> bool:
        """
        Fill an input field identified by placeholder text.
        
        Args:
            placeholder: The placeholder text of the input
            value: The value to enter
            
        Returns:
            True if successful, False otherwise
        """
        try:
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            
            for input_field in inputs:
                if placeholder.lower() in input_field.get_attribute("placeholder").lower():
                    input_field.clear()
                    input_field.send_keys(value)
                    time.sleep(0.5)
                    return True
            
            print(f"Input with placeholder '{placeholder}' not found")
            return False
        except Exception as e:
            print(f"Error filling input '{placeholder}': {e}")
            return False
    
    def test_known_animal(self, animal_name: str, answers: List[bool]) -> bool:
        """
        Test the game with a known animal by providing a sequence of answers.
        
        Args:
            animal_name: The expected animal name to be guessed
            answers: List of boolean answers (True for Yes, False for No)
            
        Returns:
            True if the test passed, False otherwise
        """
        try:
            print(f"\n=== Testing known animal: {animal_name} ===")
            
            initial_score = self._get_score_info()
            print(f"Initial session score: {initial_score['session_score']}")
            
            for i, answer in enumerate(answers):
                question = self._get_current_question()
                print(f"Question {i+1}: {question}")
                print(f"Answer: {'Yes' if answer else 'No'}")
                
                # Click Yes or No button
                if answer:
                    if not self._click_button("Yes"):
                        print(f"Failed to click Yes button")
                        return False
                else:
                    if not self._click_button("No"):
                        print(f"Failed to click No button")
                        return False
                
                time.sleep(1)
            
            # Check if the guessed animal is correct
            final_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            if animal_name.lower() in final_text.lower():
                print(f"✓ Successfully guessed: {animal_name}")
                
                # Check for score display
                if "earned" in final_text.lower() and "points" in final_text.lower():
                    print(f"✓ Score information displayed")
                
                # Verify score increased
                current_score = self._get_score_info()
                expected_score = initial_score['session_score'] + (len(answers) * 10)
                if current_score['session_score'] >= expected_score:
                    print(f"✓ Score updated correctly: {current_score['session_score']} points")
                else:
                    print(f"⚠ Score may not have updated as expected: {current_score['session_score']} vs expected {expected_score}")
                
                # Click "Yes, you got it!" to confirm
                if self._click_button("Yes, you got it!"):
                    time.sleep(2)
                    print("✓ Confirmed correct guess")
                    return True
            
            print(f"✗ Failed to guess {animal_name}")
            return False
            
        except Exception as e:
            print(f"Error in test_known_animal: {e}")
            return False
    
    def test_new_animal_learning(self, answers: List[bool], new_animal: str, 
                                distinguishing_question: str, answer_for_new: bool) -> bool:
        """
        Test teaching the system a new animal.
        
        Args:
            answers: Initial answers leading to a wrong guess
            new_animal: The correct animal name
            distinguishing_question: Question to distinguish the new animal
            answer_for_new: Answer to the question for the new animal
            
        Returns:
            True if learning succeeded, False otherwise
        """
        try:
            print(f"\n=== Testing new animal learning: {new_animal} ===")
            
            # Answer questions until we get a guess
            for i, answer in enumerate(answers):
                question = self._get_current_question()
                print(f"Question {i+1}: {question}")
                
                if answer:
                    self._click_button("Yes")
                else:
                    self._click_button("No")
                
                time.sleep(1)
            
            # Check for "lost points" message
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            if "lost" in body_text.lower() and "points" in body_text.lower():
                print("✓ Loss penalty message displayed")
            
            # Click "No, wrong guess"
            if not self._click_button("No, wrong guess"):
                print("Failed to click 'No, wrong guess'")
                return False
            
            time.sleep(2)
            
            # Fill in the learning form
            print(f"Teaching: {new_animal}")
            
            if not self._fill_input("e.g., Lion", new_animal):
                print("Failed to enter animal name")
                return False
            
            if not self._fill_input("e.g., Does it live", distinguishing_question):
                print("Failed to enter distinguishing question")
                return False
            
            time.sleep(1)
            
            # Select the appropriate radio button
            # This is more complex with Streamlit - we may need to click on the label
            radio_labels = self.driver.find_elements(By.TAG_NAME, "label")
            target_text = "Yes / True" if answer_for_new else "No / False"
            
            for label in radio_labels:
                if target_text in label.text:
                    label.click()
                    time.sleep(0.5)
                    break
            
            # Submit the form
            if not self._click_button("Teach Me"):
                print("Failed to click 'Teach Me'")
                return False
            
            time.sleep(2)
            
            # Check for success message
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            if "remember" in body_text.lower() or "success" in body_text.lower():
                print(f"✓ Successfully taught new animal: {new_animal}")
                
                # Click "Play Again" button
                if self._click_button("Play Again"):
                    time.sleep(2)
                    print("✓ Started new game after learning")
                
                return True
            
            print("✗ Failed to teach new animal")
            return False
            
        except Exception as e:
            print(f"Error in test_new_animal_learning: {e}")
            return False
    
    def test_new_game_button(self) -> bool:
        """
        Test the 'New Game' button functionality.
        
        Returns:
            True if the button works correctly, False otherwise
        """
        try:
            print("\n=== Testing New Game button ===")
            
            initial_score = self._get_score_info()
            print(f"Session score before new game: {initial_score['session_score']}")
            
            # Answer a question first
            self._click_button("Yes")
            time.sleep(1)
            
            # Verify score increased
            after_answer_score = self._get_score_info()
            if after_answer_score['session_score'] > initial_score['session_score']:
                print(f"✓ Score increased after answering: {after_answer_score['session_score']}")
            
            # Click New Game in sidebar
            if not self._click_button("New Game"):
                print("Failed to click 'New Game'")
                return False
            
            time.sleep(2)
            
            # Verify session score was reset to 0
            new_game_score = self._get_score_info()
            if new_game_score['session_score'] == 0:
                print(f"✓ Session score reset to 0")
            else:
                print(f"⚠ Session score not reset: {new_game_score['session_score']}")
            
            # Verify we're back at the start
            question = self._get_current_question()
            if question:
                print(f"✓ New Game button works correctly - restarted with question: {question}")
                return True
            
            print("✗ New Game button did not reset properly")
            return False
            
        except Exception as e:
            print(f"Error in test_new_game_button: {e}")
            return False
    
    def run_all_tests(self) -> bool:
        try:
            print(f"\n{'='*60}")
            print("Starting E2E Tests for Animal Oracle")
            print(f"{'='*60}")
            
            self.driver = self._init_driver()
            self.driver.get(self.base_url)
            self._wait_for_streamlit_ready()
            
            print(f"Connected to: {self.base_url}")
            print(f"Page title: {self.driver.title}")
            
            # Login first
            if not self._login():
                print("✗ Login failed - cannot proceed with tests")
                return False
            
            results = []
            
            # Test 1: Known animal - Dog
            results.append(self.test_known_animal("Dog", [True, True, True, True]))
            
            # Reset for next test
            self._click_button("New Game")
            time.sleep(2)
            
            # Test 2: Known animal - Cat
            results.append(self.test_known_animal("Cat", [True, True, True, False]))
            
            # Reset for next test
            self._click_button("New Game")
            time.sleep(2)
            
            # Test 3: New Game button
            results.append(self.test_new_game_button())
            
            # Reset for next test
            self._click_button("New Game")
            time.sleep(2)
            
            # Test 4: Learning a new animal
            results.append(self.test_new_animal_learning(
                answers=[True, True, False, True],  # Leads to Hamster
                new_animal="Ferret",
                distinguishing_question="Is it long and slender?",
                answer_for_new=True
            ))
            
            # Print summary
            print(f"\n{'='*60}")
            print("Test Summary")
            print(f"{'='*60}")
            print(f"Tests passed: {sum(results)}/{len(results)}")
            
            # Show final score info
            final_score = self._get_score_info()
            print(f"\nFinal Scores:")
            print(f"  Session Score: {final_score['session_score']}")
            print(f"  Total Score: {final_score['total_score']}")
            print(f"  Questions Asked: {final_score['questions_asked']}")
            
            all_passed = all(results)
            if all_passed:
                print("\n✓ All tests PASSED!")
            else:
                print("\n✗ Some tests FAILED")
            
            return all_passed
            
        except Exception as e:
            print(f"Error in run_all_tests: {e}")
            return False
        finally:
            if self.driver:
                print("\nClosing browser...")
                time.sleep(2)
                self.driver.quit()

if __name__ == "__main__":
    # Run the tests with a test username
    test = Test_E2E(base_url="http://localhost:8501", username="E2E_TestUser")
    success = test.run_all_tests()
    
    exit(0 if success else 1)
        
