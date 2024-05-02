package services
import java.net.{HttpURLConnection, URL, URLEncoder}
import java.io.{BufferedReader, InputStreamReader}

object API {
  def sendToAPI(reviewText: String): (String, String) = {
    // URL of the API endpoint
    val baseUrl = "http://localhost:5000/rate-comment"
    val url = new URL(baseUrl + s"?comment=${URLEncoder.encode(reviewText, "UTF-8")}")

    // Make GET request to the API
    val connection = url.openConnection.asInstanceOf[HttpURLConnection]
    connection.setRequestMethod("POST")

    // Check response code
    val responseCode = connection.getResponseCode
    if (responseCode == HttpURLConnection.HTTP_OK) {
      val inputStream = new BufferedReader(new InputStreamReader(connection.getInputStream))
      val response = new StringBuilder
      var inputLine: String = inputStream.readLine()
      while (inputLine != null) {
        response.append(inputLine)
        inputLine = inputStream.readLine()
      }
      inputStream.close()
      (reviewText, response.toString)
    } else {
      val errorStream = new BufferedReader(new InputStreamReader(connection.getErrorStream))
      val errorMessage = new StringBuilder
      var errorLine: String = errorStream.readLine()
      while (errorLine != null) {
        errorMessage.append(errorLine)
        errorLine = errorStream.readLine()
      }
      errorStream.close()
      throw new Exception(s"Failed to publish message: HTTP $responseCode - $errorMessage")
    }
  }

  // Function to process API response
  def processResponse(response: (String, String)): Unit = {
    return (response._1,response._2)

    println(s"API Response for `${response._1}`: " + response._2)
    // Add your processing logic here
//    s"API Response for `$text`: " + response
  }
}
