class TaskDefinition(object):
	def __init__(self):
		self.type = 'task_def'
		self.name = ''
		self.args = []
		
class MoveCommand(object):
	def __init__(self):
		self.type = 'move'
		self.resource = ''
		self.point = []
		self.offset_point = []
		self.speed = []
		self.time = []
		self.interpolation = 0
		self.wait_interpolation = True
		self.velocity = []
		self.velocity_time = []

class CodeParser(object):

	def __init__(self):
		self.header = ''
		self.footer = ''

	def WriteFile(self, file_name = "foo.txt"):
		# Open a file
		fo = open(file_name, "wb")
		fo.write( "Define SortEncoderBaseFromBin <arg1> <arg2>\n");
		fo.write( "Move larm to [point_a, point_b] shifted [offset_a, offset_b] at [1.0, 2.0]\n");
		fo.write( "Move larm to point_a shifted offset_a at 1.0\n");
		fo.write( "Move larm to [point a, point_b\n");
		fo.write( "Move larm to point a\n");
		fo.write( "Move larm\n");
		# Close opend file
		fo.close()

	def ParseLine(self, line):
		line = line.strip("\n")
		
		parsed_line = line.split(' ')	


		if parsed_line[0] == 'Define':
			task_def = TaskDefinition()
			task_def.name = parsed_line[1]

			for i in xrange(2, len(parsed_line)):
				arg = parsed_line[i].strip('<').strip('>')
				task_def.args.append(arg)

			return task_def

		if parsed_line[0] == 'Move':

			move = MoveCommand()
			move.resource = parsed_line[1]

			try:
				index = parsed_line.index('to')
				tmp = ''
				for i in xrange(index+1, len(parsed_line)):
					if parsed_line[i].find('shifted') == 0:
						break
					if parsed_line[i].find('at') == 0:
						break
					tmp = tmp + parsed_line[i]

				move.point = tmp.strip('[').strip(']').split(',')

			except ValueError:
				print '[Error] Destination not specified'
				return False

			try:
				index = parsed_line.index('shifted')
				tmp = ''
				for i in xrange(index+1, len(parsed_line)):
					if parsed_line[i].find('at') == 0:
						break
					tmp = tmp + parsed_line[i]

				move.offset_point = tmp.strip('[').strip(']').split(',')

			except ValueError:
				tmp = []
				for x in xrange(0, len(move.point)):
					tmp.append("no offset")
					move.offset_point = tmp

			try:
				index = parsed_line.index('at')
				tmp = ''
				for i in xrange(index+1, len(parsed_line)):
					tmp = tmp + parsed_line[i]

				move.speed = tmp.strip('[').strip(']').split(',')

			except ValueError:
				tmp = []
				for x in xrange(0, len(move.point)):
					tmp.append('1.0')
					move.speed = tmp

			#print (move.point)
			#print (move.offset_point)
			#print (move.speed)

			return move

	def AlgToJSON(self, alg):

		ret = "{"
		if alg.type == 'move':
			#print "Move Command"

			if len(alg.point) > 1:
				ret += '"Mooove": '
			else:
				ret += '"Move": {'
				ret += '"point": "' + alg.point[0] + '",'
				ret += '"offset_point": "' + alg.offset_point[0] + '",'
				ret += '"speed": '
				ret += alg.speed[0]
				ret += ','				
				ret += '"resource": ["' + alg.resource + '"]}}'

		elif alg.type == 'task_def':
			#print "Task Definition"

			self.header = '{\n "name": "' + alg.name + '",\n'
			self.header += '"program": [[[\n' 

			self.footer = ']]]}\n'

			ret = ""

		#print ret
		return ret

	def ConvertAlgToJSONFile(self, input_file="test_alg.txt", output_file = "TestAlg.json"):
		print "This is a test run conversion"


		lines = self.ReadFile(input_file)

		ret = []
		for x in xrange(0, len(lines)):
			ret.append(self.AlgToJSON(self.ParseLine(lines[x])))

		fo = open(output_file, "wb")
		fo.write(self.header)

		for x in xrange(0, len(ret)):
			fo.write(ret[x] + '\n')
		fo.write(self.footer)

		fo.close()
		return True

	def ReadFile(self, file_name="test_alg.txt"):
		# Open a file
		with open(file_name, "r") as f:
			data = f.readlines()

			lines = []
			for line in data:
				lines.append(line)

		return lines

if __name__=='__main__':
	cp = CodeParser()
	#cp.WriteFile()
	cp.ReadFile()
