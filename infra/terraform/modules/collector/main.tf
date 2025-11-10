resource "docker_image" "collector" {
  name = "collector:local"
  build {
    context    = abspath("${path.module}/../../../../")
    dockerfile = "src/collector/dockerfile" 
  }
}

resource "docker_container" "collector" {
  name  = "collector"
  image = docker_image.collector.image_id
  restart = "unless-stopped"
  ports {
    internal = 8000
    external = 8080
  }
}
