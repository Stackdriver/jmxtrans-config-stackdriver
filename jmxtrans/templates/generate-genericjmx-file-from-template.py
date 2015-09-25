#!/usr/bin/env python

import re
import simplejson as json
from collections import OrderedDict

def camel_to_snake(camel_var):
    """ Take a string in CamelCase and return it in snake_case 
    """
    step1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_var)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', step1).lower()


def convert_tmpl_to_genericjmx(plugin_name, tmpl_content):
  """ Walk the tmpl file structures and build out a string with the
      content for the GenericJMX config file

      :param plugin_name: used to alias the plugin in the chain statements, and prefix bean names
      :param tmpl_content: dict (from JSON tmpl file) with the bean/attribute definitions
  """
  out_content = []

  # header
  out_content.append('\n'.join([ 
  '# Look for JMX_HOST and JMX_PORT to adjust your configuration file.' ,
  '',
  'LoadPlugin java',
  '<Plugin "java">',
  '    JVMARG "-Djava.class.path=/opt/stackdriver/collectd/share/collectd/java/collectd-api.jar:/opt/stackdriver/collectd/share/collectd/java/generic-jmx.jar"',
  '    LoadPlugin "org.collectd.java.GenericJMX"',
  '',
  '    <Plugin "GenericJMX">'
  ]))

  mbean_connections = []

  for query in tmpl_content.get('queryInfos', []):
      mbean_alias =  query['resultAlias'].lower().replace('.', '_')
      mbean_alias_short = mbean_alias.rsplit('_', 1)[1]
      mbean_connections.append('            Collect "%s"' % mbean_alias)

      query_text = []
      # bean info
      query_text.append('\n'.join([
      '        <MBean "%s">' % mbean_alias,
      '            ObjectName "%s"' % query['obj']
      ]))

      # do each attribute as a value block
      for attr in query['attr']:
          attr_snake = camel_to_snake(attr) 
          value_text = []
          value_text.append('\n'.join([
            '            <Value>',
            '                Type "gauge"',
            '                InstancePrefix "%s-%s"' % (mbean_alias_short, attr_snake,),
            '                Table false',
            '                Attribute "%s"' % attr,
            '            </Value>'
          ]))
          
          query_text.append('\n'.join(value_text))

      # bean footer
      query_text.append('        </MBean>')
      out_content.append('\n'.join(query_text))

  # connection block, all bean names
  out_content.append('\n'.join([
  '        <Connection>',
  '            ServiceURL "service:jmx:rmi:///jndi/rmi://JMX_HOST:JMX_PORT/jmxrmi"',
  '            InstancePrefix "%s"' % plugin_name,
  ''
  ]))
  out_content.append('\n'.join(mbean_connections))
  out_content.append('        </Connection>')

  # file footer
  out_content.append('\n'.join([
  '    </Plugin>',
  '</Plugin>',
  '',
  'LoadPlugin match_regex',
  'LoadPlugin target_set',
  'LoadPlugin target_replace',
  '<Chain "GenericJMX_%s">' % plugin_name,
  '    <Rule "rewrite_genericjmx_to_%s">' % plugin_name,
  '        <Match regex>',
  '            Plugin "^GenericJMX$"',
  '            PluginInstance "%s.*"' % plugin_name,
  '        </Match>',
  '        <Target "set">',
  '            Plugin "%s"' % plugin_name,
  '        </Target>',
  '        <Target "replace">',
  '            PluginInstance "%s" ""' % plugin_name,
  '        </Target>',
  '        Target "return"',
  '    </Rule>',
  '</Chain>',
  '',
  '<Chain "PreCache">',
  '    <Rule "jump_to_GenericJMX_%s">' % plugin_name,
  '        <Target "jump">',
  '            Chain "GenericJMX_%s"' % plugin_name,
  '        </Target>',
  '    </Rule>',
  '</Chain>',
  'PreCacheChain "PreCache"'
  ]))

  return '\n'.join(out_content)


def main():
  """ Convert a simple .tmpl file with JMX bean and attribute names, and output an initial
      pass at a GenericJMX plugin config file to collect those beans.

      ARGUMENTS:

      plugin - plugin alias that this instance of GenericJMX will be renamed to using chain
      source - the *.tmpl file with the mBean attribute definitions
      output - the *.conf GenericJMX file that will be written.

      NOTES ON OUTPUT FILES:

      The output file will not account for InstanceFrom statements (with wildcards) such as
      in JVM garbage collectors.

      All variables will be marked as "gauge" but some may need to be set to "counter" where
      appropriate.

      This still does 90% of the work.
  """
  
  import sys
  import argparse
 
  parser = argparse.ArgumentParser()
  parser.add_argument('-p', '--plugin', help='The name of the service (jvm, cassandra, etc)')
  parser.add_argument('-s', '--source', help='The source TMPL file path')
  parser.add_argument('-o', '--output', help='The output GenericJMX conf file path')
  opts = parser.parse_args()
 
  print('--- generating GenericJMX conf from tmpl, input file: %s' % opts.source)
  
  with open(opts.source) as in_file:
    tmpl_content = json.load(in_file, object_pairs_hook=OrderedDict)
  
  genericjmx_content = convert_tmpl_to_genericjmx(opts.plugin, tmpl_content)
  
  print('--- writing ./%s' % opts.output)
  with open(opts.output, 'wb') as out_file:
    out_file.write(genericjmx_content)
 
 
if __name__ == '__main__':
  main()