resource "aws_cloudfront_distribution" "cdn" {
  origin {
    domain_name = "origin.${var.r53_public_hosted_zone}"
    origin_id   = "originAlb"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1", "TLSv1.1", "TLSv1.2"]
    }
  }

  enabled         = true
  is_ipv6_enabled = true
  http_version    = "http2"
  comment         = "${var.project} (${var.environment})"

  price_class = "${var.cloudfront_price_class}"
  aliases     = ["${var.r53_public_hosted_zone}"]

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "originAlb"

    forwarded_values {
      query_string = true
      headers      = ["*"]

      cookies {
        forward = "all"
      }
    }

    compress               = false
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 0
    max_ttl                = 300

    ## This feature is only available in Terraform AWS Provider 3.41.0 and later
    # function_association {
    #   event_type   = "viewer-request"
    #   function_arn = "${aws_cloudfront_function.oshub_conditional_redirect.arn}"
    # }
  }

  ordered_cache_behavior {
    path_pattern     = "static/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "originAlb"

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    compress               = true
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 300
    max_ttl                = 300
  }

  ordered_cache_behavior {
    path_pattern     = "tile/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "originAlb"

    forwarded_values {
      query_string = true
      headers      = ["Referer"] # To discourage hotlinking to cached tiles

      cookies {
        forward = "none"
      }
    }

    compress               = true
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 31536000            # 1 year. Same as TILE_CACHE_MAX_AGE_IN_SECONDS in src/django/oar/settings.py
  }

  logging_config {
    include_cookies = false
    bucket          = "${aws_s3_bucket.logs.bucket_domain_name}"
    prefix          = "CDN"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = "${module.cert_cdn.arn}"
    minimum_protocol_version = "TLSv1.2_2018"
    ssl_support_method       = "sni-only"
  }

  tags {
    Project     = "${var.project}"
    Environment = "${var.environment}"
  }
}


## This resource is only available in Terraform AWS Provider 3.41.0 and later
# resource "aws_cloudfront_function" "oshub_conditional_redirect" {
#   name    = "cffn${replace(var.project, " ", "")}${var.environment}OSHubConditionalRedirect"
#   runtime = "cloudfront-js-1.0"
#   comment = "Redirect non-embedded map traffic to opensupplyhub.org"
#   publish = true
#   code    = "${file("cloudfront-functions/conditional_oshub_redirect.js")}"
# }
