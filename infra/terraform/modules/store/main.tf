resource "docker_volume" "store_data" {
  name = "store_data"
}

resource "docker_image" "store" {
  name = "store:local"
  build {
    context    = abspath("${path.module}/../../../../")
    dockerfile = "src/store/dockerfile"
  }
}

resource "docker_container" "store" {
  name  = "store"
  image = docker_image.store.image_id
  restart = "unless-stopped"
  ports {
    internal = 8000
    external = 8081
  }
  volumes {
    volume_name = docker_volume.store_data.name
    container_path  = "/app/data"
  }
}
