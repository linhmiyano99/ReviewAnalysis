package services

object API {
  def sendToAPI(reviewText: String): String = {
  //  val apiUrl = "YOUR_API_URL" // Replace with your API URL
  //  val response: HttpResponse[String] = Http(apiUrl).postData(reviewText).asString
  //  response.body
      "sendToAPI"
  }

  // Function to process API response
  def processResponse(response: String): Unit = {
    println("API Response: " + response)
    // Add your processing logic here
  }
}
