resource "docker_volume" "viewer_data" {
  name = "store_data"
}

resource "docker_image" "viewer" {
  name = "viewer:local"
  build {
    context    = abspath("${path.module}/../../../../")
    dockerfile = "src/viewer/dockerfile"
  }
}

resource "docker_container" "viewer" {
  name    = "viewer"
  image   = docker_image.viewer.image_id
  restart = "unless-stopped"
  ports {
    internal = 8000
    external = 8082
  }
  volumes {
    volume_name = docker_volume.viewer_data.name
    container_path  = "/app/data"
  }
}