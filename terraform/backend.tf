terraform {
  backend "s3" {
    bucket = "oficina10-terraform"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}