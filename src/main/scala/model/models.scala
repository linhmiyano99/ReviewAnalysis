package model
package object models{
  case class Review (reviewId: String, asin: String, reviewName: String, helpful: Array[Int], reviewText: String, overall: Float, summary: String, unixReviewTime: Int, reviewTime: String){}
}