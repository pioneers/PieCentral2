import path from 'path';
import webpack from 'webpack';
import { version } from './package.json';

const target = 'electron';
const modules = {
  preLoaders: [
    {
      test: /\.js$/,
      exclude: /node_modules/,
      loader: 'eslint-loader',
    },
  ],
  loaders: [
    {
      test: /\.js$/,
      exclude: /node_modules/,
      loader: 'babel-loader',
    },
    {
      test: /\.json$/,
      loader: 'json-loader',
    },
  ],
};

const plugins = [
  new webpack.DefinePlugin({
    VERSION: JSON.stringify(version),
  }),
  new webpack.DefinePlugin({
    'global.GENTLY': false,
  }),
  new webpack.EnvironmentPlugin(['NODE_ENV']),
];

export default [
  {
    entry: './renderer/index.js',
    devtool: 'cheap-module-eval-source-map',
    output: {
      path: path.join(__dirname, 'build'),
      filename: 'bundle.js',
    },
    target,
    module: modules,
    plugins,
  },
  {
    entry: './main/main-develop.js',
    output: {
      path: path.join(__dirname, 'build'),
      filename: 'main.js',
    },
    target,
    node: {
      __dirname: false,
      __filename: false,
    },
    module: modules,
    plugins,
  },
];
