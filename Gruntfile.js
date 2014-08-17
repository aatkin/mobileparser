module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        nose: {
            options: {
                virtualenv: 'env'
            },
            main: {}
        },
        watch: {
            gruntfile: {
                files: 'Gruntfile.js'
            },
            pythonNose: {
                files: ['tests/**/*.py'],
                tasks: ['nose']
            }
        }

    });

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-nose');

    grunt.registerTask('default', ['watch']);
}