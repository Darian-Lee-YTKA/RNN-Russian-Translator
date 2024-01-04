//
//  translationVC.swift
//  simple_translator
//
//  Created by Darian Lee on 1/3/24.
//

import UIKit

class translationVC: UIViewController {
    
    @IBOutlet weak var userText: UITextField!
    @IBOutlet weak var translateButton: UIButton!
    @IBOutlet weak var translation: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        translateButton.layer.cornerRadius = 8
        translation.text = ""
        // Do any additional setup after loading the view.
    }
    
    
    @IBAction func didPressTranslate(_ sender: UIButton){
            print("did press translate")
        guard let text = userText.text else {
                    print("no input")
                    return
                }
            let punctuationCharacterSet = CharacterSet.punctuationCharacters

            // I forgot to remove the punctuation in the python code, so I'll do it here
            let textWithoutPunctuation = String(text.unicodeScalars.filter { !punctuationCharacterSet.contains($0) })

            print("Original Text: \(text)")
            print("Text Without Punctuation: \(textWithoutPunctuation)")
        print(userText.text!)

                translateText(with: textWithoutPunctuation) { translatedText in
                    DispatchQueue.main.async {
                        if let translatedText = translatedText {
                            print("translation worked")
                            self.translation.text = translatedText
                            print("this is the translation \(translatedText)")
                        } else {
                            print("Translation failed or returned nil")
                        }
                    }
                }
            }
    
    
    func translateText(with text: String, completion: @escaping (String?) -> Void) {
            let url = URL(string: "http://127.0.0.1:5000/SimpleTranslate")!

            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.addValue("application/json", forHTTPHeaderField: "Content-Type")

            let payload: [String: String] = ["text": text]

            do {
                let jsonData = try JSONSerialization.data(withJSONObject: payload, options: [])

                request.httpBody = jsonData
            } catch {
                print("Error converting payload to JSON: \(error)")
                completion(nil)
                return
            }

            let task = URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    print("Error: \(error)")
                    completion(nil)
                    return
                }


                guard let data = data else {
                    print("No data received.")
                    completion(nil)
                    return
                }

                do {
                    let jsonResponse = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]

  
                    if let translation = jsonResponse?["translation"] as? String {
                        completion(translation)
                    } else {
                        print("Unexpected response format.")
                        completion(nil)
                    }
                } catch {
                    print("Error parsing JSON response: \(error)")
                    completion(nil)
                }
            }

            // Start the task
            task.resume()
            
        }

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
