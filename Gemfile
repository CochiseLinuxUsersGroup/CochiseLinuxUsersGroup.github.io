source 'https://rubygems.org'

require 'json'
require 'open-uri'
begin
  versions = JSON.parse(URI.open('https://pages.github.com/versions.json').read)
  gem 'github-pages', versions['github-pages']
rescue StandardError => e
  # Fallback for offline/local builds - use latest github-pages compatible gems
  warn "Could not fetch GitHub Pages versions: #{e.message} - using fallback gems"
  gem 'github-pages', group: :jekyll_plugins
end

gem 'webrick', '~> 1.8'

group :jekyll_plugins do
  gem 'jekyll-feed', '~> 0.17'
  gem 'jekyll-sitemap', '~> 1.4'
  gem 'jekyll-seo-tag', '~> 2.8'
  gem 'jekyll-paginate', '~> 1.1'
end

