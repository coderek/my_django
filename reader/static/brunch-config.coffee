exports.config =
  # See http://brunch.io/#documentation for docs.
  files:
    javascripts:
      joinTo: 'scripts/app.js'
      order:
        before: [
          'bower_components/jquery/dist/jquery.js'
        ]
    stylesheets:
      joinTo:
        'styles/app.css': 'app/styles/*'
        'styles/vender.css': 'bower_components/bootstrap/dist/css/bootstrap.css'
    templates:
      joinTo: 'scripts/app.js'

  paths:
    public: './reader'

  plugins:
    babel:
      presets: ['es2015']
      ignore: [
        /^(bower_components|vendor)/
        'app/legacyES5Code/**/*'
      ]
      pattern: /\.(es6|jsx)$/

