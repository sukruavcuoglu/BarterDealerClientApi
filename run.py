from application import create_app

config_name = "production"
connex_app = create_app(config_name)


# def get_bundled_specs(main_file: Path) -> Dict[str, Any]:
#     parser = prance.ResolvingParser(str(main_file.absolute()),
#                                     lazy=True, strict=False, backend='openapi-spec-validator')
#     parser.parse()
#     return parser.specification


# Read the swagger_user.yml file to configure the endpoints
connex_app.add_api("swagger_user.yml")
# connex_app.add_api("swagger_category.yml")
# connex_app.add_api(get_bundled_specs(Path("swagger_user.yml")))
# connex_app.add_api(get_bundled_specs(Path("swagger_category.yml")))

app = connex_app.app

if __name__ == '__main__':
    connex_app.run(debug=True)
