'use strict';

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up (queryInterface, Sequelize) {
   await queryInterface.createTable('test', { id: Sequelize.INTEGER });
  },

  async down (queryInterface, Sequelize) {
    await queryInterface.dropTable('test');
  }
};
